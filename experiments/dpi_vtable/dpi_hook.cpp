// Standalone Mari DPI experiment. This DLL contains no localization hooks.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QDateTime>
#include <QtCore/QEvent>
#include <QtCore/QFile>
#include <QtCore/QMetaObject>
#include <QtCore/QPointer>
#include <QtCore/QTextStream>
#include <QtCore/QTimer>
#include <QtWidgets/QApplication>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QWidget>

#include <atomic>
#include <vector>

namespace {

using QWidgetMetricFn = int (__cdecl *)(const QWidget *, int);
using ResizeGlFn = void (__cdecl *)(QWidget *, int, int);

struct CanvasPatch {
    void **vtable = nullptr;
    QWidgetMetricFn originalMetric = nullptr;
    ResizeGlFn originalResizeGl = nullptr;
};

constexpr qreal kCanvasDevicePixelRatio = 1.0;
constexpr int kOrthoResizeMultiplier = 2;
constexpr qint64 kMaxLogBytes = 4 * 1024 * 1024;

HINSTANCE g_instance = nullptr;
SRWLOCK g_patchLock = SRWLOCK_INIT;
std::vector<CanvasPatch> g_canvasPatches;
std::vector<QPointer<QWidget>> g_observedWidgets;
int g_metricIndex = -1;
int g_resizeGlIndex = -1;
std::vector<int> g_resizeGlCandidates;
std::atomic<int> g_orthoResizeCalls{0};
std::atomic<int> g_lastOrthoInputWidth{0};
std::atomic<int> g_lastOrthoInputHeight{0};

bool isExecutableAddress(const void *address) {
    if (!address)
        return false;
    MEMORY_BASIC_INFORMATION info{};
    if (VirtualQuery(address, &info, sizeof(info)) != sizeof(info) ||
        info.State != MEM_COMMIT ||
        (info.Protect & (PAGE_NOACCESS | PAGE_GUARD)))
        return false;
    const DWORD executable = PAGE_EXECUTE | PAGE_EXECUTE_READ |
                             PAGE_EXECUTE_READWRITE | PAGE_EXECUTE_WRITECOPY;
    return (info.Protect & executable) != 0;
}

QString dllDirectory() {
    std::vector<wchar_t> buffer(1024);
    while (buffer.size() <= 32768) {
        const DWORD size = GetModuleFileNameW(
            g_instance, buffer.data(), static_cast<DWORD>(buffer.size()));
        if (!size)
            return {};
        if (size < buffer.size() - 1) {
            const QString path = QString::fromWCharArray(buffer.data(), size);
            return path.left(path.lastIndexOf(QLatin1Char('\\')));
        }
        buffer.resize(buffer.size() * 2);
    }
    return {};
}

bool isTrackedClass(const QWidget *widget) {
    if (!widget)
        return false;
    const QByteArray className(widget->metaObject()->className());
    return className == "MriCanvasWidget" ||
           className == "MriCanvasContainer" ||
           className == "MriProjectController" ||
           className == "MriProjectListWidget";
}

bool isCanvas(const QWidget *widget) {
    return widget &&
           qstrcmp(widget->metaObject()->className(), "MriCanvasWidget") == 0;
}

bool isOrthoCanvas(const QWidget *widget) {
    QWidget *parent = widget ? widget->parentWidget() : nullptr;
    QWidget *container = parent ? parent->parentWidget() : nullptr;
    return container && container->objectName() == QStringLiteral("Ortho");
}

void discoverVtableIndices() {
    if (g_metricIndex >= 0 && g_resizeGlIndex >= 0)
        return;
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!qtWidgets)
        return;

    void *metricAddress = reinterpret_cast<void *>(GetProcAddress(
        qtWidgets,
        "?metric@QOpenGLWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z"));
    void *resizeAddress = reinterpret_cast<void *>(GetProcAddress(
        qtWidgets, "?resizeGL@QOpenGLWidget@@MEAAXHH@Z"));
    if (!metricAddress || !resizeAddress)
        return;

    g_resizeGlCandidates.clear();
    QOpenGLWidget baseProbe;
    void **baseVtable = *reinterpret_cast<void ***>(&baseProbe);
    for (int index = 0; index < 128; ++index) {
        if (g_metricIndex < 0 && baseVtable[index] == metricAddress)
            g_metricIndex = index;
        if (baseVtable[index] == resizeAddress)
            g_resizeGlCandidates.push_back(index);
    }

    // MSVC folds several empty Qt virtual functions to the same address.
    // QOpenGLWidget declares initializeGL(), resizeGL(), paintGL() consecutively;
    // identify the isolated three-slot run and select its middle member.
    for (std::size_t first = 0; first < g_resizeGlCandidates.size();) {
        std::size_t last = first;
        while (last + 1 < g_resizeGlCandidates.size() &&
               g_resizeGlCandidates[last + 1] ==
                   g_resizeGlCandidates[last] + 1)
            ++last;
        if (last - first + 1 == 3) {
            g_resizeGlIndex = g_resizeGlCandidates[first + 1];
            break;
        }
        first = last + 1;
    }
}

QWidgetMetricFn originalMetricFor(const QWidget *widget) {
    void **vtable = widget ? *reinterpret_cast<void ***>(
        const_cast<QWidget *>(widget)) : nullptr;
    AcquireSRWLockShared(&g_patchLock);
    QWidgetMetricFn result = nullptr;
    for (const CanvasPatch &patch : g_canvasPatches) {
        if (patch.vtable == vtable) {
            result = patch.originalMetric;
            break;
        }
    }
    ReleaseSRWLockShared(&g_patchLock);
    return result;
}

ResizeGlFn originalResizeGlFor(QWidget *widget) {
    void **vtable = widget ? *reinterpret_cast<void ***>(widget) : nullptr;
    AcquireSRWLockShared(&g_patchLock);
    ResizeGlFn result = nullptr;
    for (const CanvasPatch &patch : g_canvasPatches) {
        if (patch.vtable == vtable) {
            result = patch.originalResizeGl;
            break;
        }
    }
    ReleaseSRWLockShared(&g_patchLock);
    return result;
}

std::size_t patchCount() {
    AcquireSRWLockShared(&g_patchLock);
    const std::size_t result = g_canvasPatches.size();
    ReleaseSRWLockShared(&g_patchLock);
    return result;
}

int hookedMetric(const QWidget *self, int metric) {
    const auto kind = static_cast<QPaintDevice::PaintDeviceMetric>(metric);
    if (kind == QPaintDevice::PdmDevicePixelRatio)
        return static_cast<int>(kCanvasDevicePixelRatio);
    if (kind == QPaintDevice::PdmDevicePixelRatioScaled) {
        return static_cast<int>(kCanvasDevicePixelRatio *
                                QPaintDevice::devicePixelRatioFScale());
    }
    const QWidgetMetricFn original = originalMetricFor(self);
    return original ? original(self, metric) : 1;
}

void hookedResizeGl(QWidget *self, int width, int height) {
    if (isOrthoCanvas(self)) {
        g_orthoResizeCalls.fetch_add(1, std::memory_order_relaxed);
        g_lastOrthoInputWidth.store(width, std::memory_order_relaxed);
        g_lastOrthoInputHeight.store(height, std::memory_order_relaxed);
        width *= kOrthoResizeMultiplier;
        height *= kOrthoResizeMultiplier;
    }
    if (const ResizeGlFn original = originalResizeGlFor(self))
        original(self, width, height);
}

bool replaceVtableSlot(void **slot, void *replacement) {
    if (!slot || !replacement)
        return false;
    DWORD oldProtection = 0;
    if (!VirtualProtect(slot, sizeof(void *), PAGE_READWRITE, &oldProtection))
        return false;
    *slot = replacement;
    DWORD ignored = 0;
    VirtualProtect(slot, sizeof(void *), oldProtection, &ignored);
    FlushInstructionCache(GetCurrentProcess(), slot, sizeof(void *));
    return true;
}

void patchCanvas(QWidget *widget) {
    if (!isCanvas(widget))
        return;
    discoverVtableIndices();
    if (g_metricIndex < 0 || g_resizeGlIndex < 0)
        return;

    void **vtable = *reinterpret_cast<void ***>(widget);
    if (!vtable)
        return;

    AcquireSRWLockExclusive(&g_patchLock);
    for (const CanvasPatch &patch : g_canvasPatches) {
        if (patch.vtable == vtable) {
            ReleaseSRWLockExclusive(&g_patchLock);
            return;
        }
    }

    void **metricSlot = &vtable[g_metricIndex];
    void **resizeSlot = &vtable[g_resizeGlIndex];
    const auto originalMetric = reinterpret_cast<QWidgetMetricFn>(*metricSlot);
    const auto originalResize = reinterpret_cast<ResizeGlFn>(*resizeSlot);
    if (!isExecutableAddress(reinterpret_cast<void *>(originalMetric)) ||
        !isExecutableAddress(reinterpret_cast<void *>(originalResize))) {
        ReleaseSRWLockExclusive(&g_patchLock);
        return;
    }

    g_canvasPatches.push_back({vtable, originalMetric, originalResize});
    const bool metricPatched = replaceVtableSlot(
        metricSlot, reinterpret_cast<void *>(&hookedMetric));
    const bool resizePatched = replaceVtableSlot(
        resizeSlot, reinterpret_cast<void *>(&hookedResizeGl));
    if (!metricPatched || !resizePatched) {
        if (metricPatched)
            replaceVtableSlot(metricSlot, reinterpret_cast<void *>(originalMetric));
        if (resizePatched)
            replaceVtableSlot(resizeSlot, reinterpret_cast<void *>(originalResize));
        g_canvasPatches.pop_back();
    }
    ReleaseSRWLockExclusive(&g_patchLock);
}

void observeWidget(QWidget *widget) {
    if (!isTrackedClass(widget))
        return;
    for (const QPointer<QWidget> &known : g_observedWidgets) {
        if (known == widget)
            return;
    }
    g_observedWidgets.push_back(widget);
    patchCanvas(widget);
}

void pruneObservedWidgets() {
    for (auto it = g_observedWidgets.begin(); it != g_observedWidgets.end();) {
        if (*it)
            ++it;
        else
            it = g_observedWidgets.erase(it);
    }
}

class WidgetLifecycleFilter final : public QObject {
public:
    using QObject::QObject;

    bool eventFilter(QObject *object, QEvent *event) override {
        if (event->type() == QEvent::Polish || event->type() == QEvent::Show) {
            if (auto *widget = qobject_cast<QWidget *>(object))
                observeWidget(widget);
        }
        return false;
    }
};

QString historyPath() {
    return dllDirectory() + QStringLiteral("/dpi_vtable_history.log");
}

void rotateHistoryIfNeeded() {
    const QString current = historyPath();
    QFile file(current);
    if (!file.exists() || file.size() < kMaxLogBytes)
        return;
    const QString previous = current + QStringLiteral(".1");
    QFile::remove(previous);
    QFile::rename(current, previous);
}

bool writeWidgetSnapshot() {
    pruneObservedWidgets();
    rotateHistoryIfNeeded();
    QFile output(historyPath());
    if (!output.open(QIODevice::Append | QIODevice::Text))
        return false;

    QTextStream stream(&output);
    stream << "--- " << QDateTime::currentDateTime().toString(Qt::ISODate)
           << " metricIndex=" << g_metricIndex
           << " resizeGlCandidates=";
    for (int index : g_resizeGlCandidates)
        stream << index << ',';
    stream
           << " resizeGlIndex=" << g_resizeGlIndex
           << " orthoResizeCalls="
           << g_orthoResizeCalls.load(std::memory_order_relaxed)
           << " lastOrthoInput="
           << g_lastOrthoInputWidth.load(std::memory_order_relaxed) << 'x'
           << g_lastOrthoInputHeight.load(std::memory_order_relaxed)
           << " patchCount=" << patchCount() << " ---\n";

    int count = 0;
    for (const QPointer<QWidget> &guard : g_observedWidgets) {
        QWidget *widget = guard.data();
        if (!widget)
            continue;
        stream << "class=" << widget->metaObject()->className()
               << " ptr=0x"
               << QString::number(reinterpret_cast<quintptr>(widget), 16)
               << " object=" << widget->objectName()
               << " size=" << widget->width() << 'x' << widget->height()
               << " dpr=" << widget->devicePixelRatioF()
               << " targetDpr=" << kCanvasDevicePixelRatio
               << " visible=" << widget->isVisible()
               << " QOpenGLWidget=" << widget->inherits("QOpenGLWidget")
               << " QGLWidget=" << widget->inherits("QGLWidget");
        if (QWidget *parent = widget->parentWidget()) {
            stream << " parent=" << parent->metaObject()->className()
                   << ':' << parent->objectName();
            if (QWidget *grandparent = parent->parentWidget()) {
                stream << " grandparent=" << grandparent->metaObject()->className()
                       << ':' << grandparent->objectName();
            }
        }
        stream << '\n';
        ++count;
    }
    return count > 0;
}

void startExperiment(QApplication *app) {
    discoverVtableIndices();
    app->installEventFilter(new WidgetLifecycleFilter(app));
    for (QWidget *widget : QApplication::allWidgets())
        observeWidget(widget);

    writeWidgetSnapshot();
    auto *snapshotTimer = new QTimer(app);
    snapshotTimer->setInterval(2000);
    QObject::connect(snapshotTimer, &QTimer::timeout,
                     [] { writeWidgetSnapshot(); });
    snapshotTimer->start();
}

DWORD WINAPI worker(LPVOID) {
    QApplication *app = nullptr;
    for (int attempt = 0; attempt < 3000; ++attempt) {
        if (QCoreApplication::instance()) {
            app = qobject_cast<QApplication *>(QCoreApplication::instance());
            if (app)
                break;
        }
        Sleep(100);
    }
    if (!app)
        return 1;
    QMetaObject::invokeMethod(app, [app] { startExperiment(app); },
                              Qt::QueuedConnection);
    return 0;
}

} // namespace

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        g_instance = instance;
        DisableThreadLibraryCalls(instance);
        if (HANDLE thread = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr))
            CloseHandle(thread);
    }
    return TRUE;
}
