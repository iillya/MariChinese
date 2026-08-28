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
#include <QtCore/QtMath>
#include <QtGui/QResizeEvent>
#include <QtWidgets/QApplication>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QWidget>

#include <atomic>
#include <cstring>
#include <limits>
#include <type_traits>
#include <vector>

#include "dpi_feature.h"

namespace {

using QWidgetMetricFn = int (__cdecl *)(const QWidget *, int);
using ResizeGlFn = void (__cdecl *)(QWidget *, int, int);

struct CanvasPatch {
    void **vtable = nullptr;
    QWidgetMetricFn originalMetric = nullptr;
    ResizeGlFn originalResizeGl = nullptr;
};

constexpr qreal kCanvasDevicePixelRatio = 1.0;
constexpr qint64 kMaxLogBytes = 4 * 1024 * 1024;

HINSTANCE g_instance = nullptr;
SRWLOCK g_patchLock = SRWLOCK_INIT;
std::vector<CanvasPatch> g_canvasPatches;
std::vector<QPointer<QWidget>> g_observedWidgets;
int g_metricIndex = -1;
int g_resizeGlIndex = -1;
std::atomic<int> g_resizeCalls{0};
std::atomic<int> g_lastInputWidth{0};
std::atomic<int> g_lastInputHeight{0};
double g_scaleFactor = 2.0;
bool g_diagnosticsEnabled = false;
bool g_started = false;

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
    if (!g_instance) {
        HMODULE module = nullptr;
        if (GetModuleHandleExW(
                GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                    GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                reinterpret_cast<LPCWSTR>(&dllDirectory), &module))
            g_instance = module;
    }
    if (!g_instance)
        return {};
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
    return widget && widget->inherits("MriCanvasWidget") &&
           widget->inherits("QOpenGLWidget");
}

// MSVC represents a pointer to a virtual member function as a pointer to a
// small dispatch thunk. The thunk reads the object's vtable and jumps through
// the member's slot. Decode that semantic operation instead of assuming a Qt
// version, exported symbol spelling, or a fixed vtable index.
template <typename MemberPointer>
int decodeMsvcVirtualSlot(MemberPointer member) {
    static_assert(std::is_trivially_copyable_v<MemberPointer>);
    if constexpr (sizeof(member) < sizeof(void *))
        return -1;

    const unsigned char *entry = nullptr;
    std::memcpy(&entry, &member, sizeof(entry));
    if (!isExecutableAddress(entry))
        return -1;

    // Follow the import-style relative jump sometimes emitted for an
    // out-of-line virtual dispatch thunk.
    if (entry[0] == 0xE9) {
        std::int32_t relative = 0;
        std::memcpy(&relative, entry + 1, sizeof(relative));
        entry += 5 + relative;
        if (!isExecutableAddress(entry))
            return -1;
    }

    // mov rax, [rcx]
    if (entry[0] != 0x48 || entry[1] != 0x8B || entry[2] != 0x01)
        return -1;

    std::uint32_t byteOffset = 0;
    if (entry[3] == 0xFF && entry[4] == 0x20) {
        byteOffset = 0; // jmp qword ptr [rax]
    } else if (entry[3] == 0xFF && entry[4] == 0x60) {
        byteOffset = entry[5]; // jmp qword ptr [rax+disp8]
    } else if (entry[3] == 0xFF && entry[4] == 0xA0) {
        std::memcpy(&byteOffset, entry + 5, sizeof(byteOffset));
    } else {
        return -1;
    }

    if (byteOffset % sizeof(void *) != 0 ||
        byteOffset / sizeof(void *) >
            static_cast<std::uint32_t>((std::numeric_limits<int>::max)()))
        return -1;
    return static_cast<int>(byteOffset / sizeof(void *));
}

class VtableProbe final : public QOpenGLWidget {
public:
    using MetricMember = int (VtableProbe::*)(
        QPaintDevice::PaintDeviceMetric) const;
    using ResizeMember = void (VtableProbe::*)(int, int);

    static MetricMember metricMember() { return &VtableProbe::metric; }
    static ResizeMember resizeMember() { return &VtableProbe::resizeGL; }

protected:
    int metric(QPaintDevice::PaintDeviceMetric value) const override {
        return QOpenGLWidget::metric(value);
    }

    void resizeGL(int width, int height) override {
        Q_UNUSED(width);
        Q_UNUSED(height);
    }
};

void discoverVtableIndices() {
    if (g_metricIndex >= 0 && g_resizeGlIndex >= 0)
        return;

    const int metricIndex = decodeMsvcVirtualSlot(VtableProbe::metricMember());
    const int resizeIndex = decodeMsvcVirtualSlot(VtableProbe::resizeMember());
    if (metricIndex < 0 || resizeIndex < 0 || metricIndex == resizeIndex)
        return;

    VtableProbe probe;
    void **vtable = *reinterpret_cast<void ***>(&probe);
    if (!vtable ||
        !isExecutableAddress(vtable[metricIndex]) ||
        !isExecutableAddress(vtable[resizeIndex]))
        return;

    g_metricIndex = metricIndex;
    g_resizeGlIndex = resizeIndex;
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
    // The metric hook reports DPR=1 for every MriCanvasWidget. Keep the
    // framebuffer resize in the same coordinate system for every canvas too;
    // limiting this correction to one named view leaves all other viewports
    // rendering into only the top-left fraction of their widgets.
    g_resizeCalls.fetch_add(1, std::memory_order_relaxed);
    g_lastInputWidth.store(width, std::memory_order_relaxed);
    g_lastInputHeight.store(height, std::memory_order_relaxed);
    width = qRound(width * g_scaleFactor);
    height = qRound(height * g_scaleFactor);
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
    if (!isCanvas(widget) && !(g_diagnosticsEnabled && isTrackedClass(widget)))
        return;
    for (const QPointer<QWidget> &known : g_observedWidgets) {
        if (known == widget)
            return;
    }
    g_observedWidgets.push_back(widget);
    patchCanvas(widget);
    if (isCanvas(widget) && originalMetricFor(widget)) {
        const QPointer<QWidget> guard(widget);
        QTimer::singleShot(0, QApplication::instance(), [guard] {
            if (!guard)
                return;
            const QSize size = guard->size();
            QResizeEvent event(size, size);
            QCoreApplication::sendEvent(guard, &event);
            guard->update();
        });
    }
}

void pruneObservedWidgets() {
    for (auto it = g_observedWidgets.begin(); it != g_observedWidgets.end();) {
        if (*it)
            ++it;
        else
            it = g_observedWidgets.erase(it);
    }
}

void scanWidgets() {
    // Production keeps this low-frequency scan for canvases created after a
    // project/view switch. Prune dead QPointers here as diagnostics may be off.
    pruneObservedWidgets();
    for (QWidget *widget : QApplication::allWidgets())
        observeWidget(widget);
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
           << " resizeGlIndex=" << g_resizeGlIndex
           << " resizeCalls="
           << g_resizeCalls.load(std::memory_order_relaxed)
           << " lastInput="
           << g_lastInputWidth.load(std::memory_order_relaxed) << 'x'
           << g_lastInputHeight.load(std::memory_order_relaxed)
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

void startExperiment(QApplication *app, bool enableDiagnostics) {
    g_diagnosticsEnabled = enableDiagnostics;
    discoverVtableIndices();
    app->installEventFilter(new WidgetLifecycleFilter(app));
    scanWidgets();

    if (enableDiagnostics)
        writeWidgetSnapshot();

    // Mari creates and replaces canvas widgets while projects and views load.
    // Application-level Polish/Show events are not reliable for every native
    // canvas, so retain the proven low-frequency discovery pass.
    auto *scanTimer = new QTimer(app);
    scanTimer->setInterval(2000);
    QObject::connect(scanTimer, &QTimer::timeout,
                     [scanTimer, enableDiagnostics] {
        scanWidgets();
        if (enableDiagnostics)
            writeWidgetSnapshot();
        else if (patchCount() > 0) {
            // A vtable patch applies to every current and future instance of
            // the same canvas class. Keep the event filter for a genuinely
            // different subclass, but stop the permanent allWidgets scan.
            scanTimer->stop();
            scanTimer->deleteLater();
        }
    });
    scanTimer->start();
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
    QTimer::singleShot(0, app, [app] {
        StartMariDpiFeature(app, 2.0, true);
    });
    return 0;
}

} // namespace

void StartMariDpiFeature(QApplication *app, double scaleFactor,
                         bool enableDiagnostics) {
    if (!app || scaleFactor < 1.0 || scaleFactor > 3.0 || g_started)
        return;
    g_started = true;
    g_scaleFactor = scaleFactor;
    startExperiment(app, enableDiagnostics);
}

#ifndef MARI_DPI_EMBEDDED
BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        g_instance = instance;
        DisableThreadLibraryCalls(instance);
        if (HANDLE thread = CreateThread(nullptr, 0, worker, nullptr, 0, nullptr))
            CloseHandle(thread);
    }
    return TRUE;
}
#endif
