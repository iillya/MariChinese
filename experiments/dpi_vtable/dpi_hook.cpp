// Standalone Mari DPI experiment. No translation, style, painter, delegate,
// font-metrics or data hooks are installed by this DLL.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QDateTime>
#include <QtCore/QFile>
#include <QtCore/QMetaObject>
#include <QtCore/QTextStream>
#include <QtCore/QTimer>
#include <QtGui/QGuiApplication>
#include <QtGui/QWindow>
#include <QtWidgets/QApplication>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QWidget>

#include <set>
#include <vector>

namespace {

using QWidgetMetricFn = int (__cdecl *)(const QWidget *, int);
using ResizeGlFn = void (__cdecl *)(QWidget *, int, int);

struct VtablePatch {
    void **slot = nullptr;
    void *original = nullptr;
};

QWidgetMetricFn g_originalMetric = nullptr;
ResizeGlFn g_originalResizeGl = nullptr;
std::vector<VtablePatch> g_patches;
HINSTANCE g_instance = nullptr;
int g_metricIndex = -1;
constexpr int kResizeGlIndex = 46;
std::vector<int> g_resizeGlCandidates;
int g_orthoResizeCalls = 0;
int g_lastOrthoInputWidth = 0;
int g_lastOrthoInputHeight = 0;

qreal ratioForCanvas(const QWidget *widget) {
    Q_UNUSED(widget);
    return 1.0;
}

void locateResizeGlCandidates() {
    if (!g_resizeGlCandidates.empty())
        return;
    HMODULE widgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!widgets)
        return;
    void *resizeAddress = reinterpret_cast<void *>(GetProcAddress(
        widgets, "?resizeGL@QOpenGLWidget@@MEAAXHH@Z"));
    if (!resizeAddress)
        return;
    QOpenGLWidget base;
    void **baseVtable = *reinterpret_cast<void ***>(&base);
    // Qt implements initializeGL(), paintGL() and resizeGL() with the same
    // empty stub. Record every matching runtime-vtable slot; their declaration
    // order will identify resizeGL without relying on an external SDK layout.
    for (int index = 0; index < 128; ++index) {
        if (baseVtable[index] == resizeAddress)
            g_resizeGlCandidates.push_back(index);
    }
}

QString dllDirectory() {
    std::vector<wchar_t> buffer(1024);
    for (;;) {
        const DWORD size = GetModuleFileNameW(g_instance, buffer.data(),
                                             static_cast<DWORD>(buffer.size()));
        if (!size) return {};
        if (size < buffer.size() - 1) {
            QString path = QString::fromWCharArray(buffer.data(), size);
            return path.left(path.lastIndexOf(QLatin1Char('\\')));
        }
        buffer.resize(buffer.size() * 2);
    }
}

int hookedMetric(const QWidget *self, int metric) {
    const auto kind = static_cast<QPaintDevice::PaintDeviceMetric>(metric);
    const qreal ratio = ratioForCanvas(self);
    if (kind == QPaintDevice::PdmDevicePixelRatio)
        return ratio >= 2.0 ? static_cast<int>(ratio) : 1;
    if (kind == QPaintDevice::PdmDevicePixelRatioScaled)
        return static_cast<int>(ratio * QPaintDevice::devicePixelRatioFScale());
    return g_originalMetric ? g_originalMetric(self, metric) : 1;
}

bool isOrthoCanvas(const QWidget *widget) {
    QWidget *parent = widget ? widget->parentWidget() : nullptr;
    QWidget *container = parent ? parent->parentWidget() : nullptr;
    return container && container->objectName() == QStringLiteral("Ortho");
}

void hookedResizeGl(QWidget *self, int width, int height) {
    if (isOrthoCanvas(self)) {
        ++g_orthoResizeCalls;
        g_lastOrthoInputWidth = width;
        g_lastOrthoInputHeight = height;
        width *= 2;
        height *= 2;
    }
    if (g_originalResizeGl)
        g_originalResizeGl(self, width, height);
}

void scanOpenGlWidgets() {
    HMODULE widgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!widgets || !QApplication::instance())
        return;
    void *metricAddress = reinterpret_cast<void *>(GetProcAddress(
        widgets,
        "?metric@QOpenGLWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z"));
    if (!metricAddress)
        return;
    g_originalMetric = reinterpret_cast<QWidgetMetricFn>(metricAddress);

    if (g_metricIndex < 0) {
        QOpenGLWidget probe;
        void **probeVtable = *reinterpret_cast<void ***>(&probe);
        for (int index = 0; index < 128; ++index) {
            if (probeVtable[index] == metricAddress) {
                g_metricIndex = index;
                break;
            }
        }
    }
    if (g_metricIndex < 0)
        return;

    std::set<void **> visited;
    for (QWidget *widget : QApplication::allWidgets()) {
        if (!widget ||
            qstrcmp(widget->metaObject()->className(), "MriCanvasWidget") != 0)
            continue;
        QWidget *parent = widget->parentWidget();
        QWidget *container = parent ? parent->parentWidget() : nullptr;
        const QString viewName = container ? container->objectName() : QString();
        void **vtable = *reinterpret_cast<void ***>(widget);
        if (!vtable || !visited.insert(vtable).second)
            continue;
        void **slot = &vtable[g_metricIndex];
        if (*slot != reinterpret_cast<void *>(&hookedMetric)) {
            DWORD oldProtection = 0;
            if (VirtualProtect(slot, sizeof(void *), PAGE_READWRITE, &oldProtection)) {
                g_originalMetric = reinterpret_cast<QWidgetMetricFn>(*slot);
                g_patches.push_back({slot, *slot});
                *slot = reinterpret_cast<void *>(&hookedMetric);
                DWORD ignored = 0;
                VirtualProtect(slot, sizeof(void *), oldProtection, &ignored);
                FlushInstructionCache(GetCurrentProcess(), slot, sizeof(void *));
            }
        }
        void **resizeSlot = &vtable[kResizeGlIndex];
        if (*resizeSlot != reinterpret_cast<void *>(&hookedResizeGl)) {
            DWORD oldProtection = 0;
            if (VirtualProtect(resizeSlot, sizeof(void *), PAGE_READWRITE,
                               &oldProtection)) {
                g_originalResizeGl = reinterpret_cast<ResizeGlFn>(*resizeSlot);
                g_patches.push_back({resizeSlot, *resizeSlot});
                *resizeSlot = reinterpret_cast<void *>(&hookedResizeGl);
                DWORD ignored = 0;
                VirtualProtect(resizeSlot, sizeof(void *), oldProtection, &ignored);
                FlushInstructionCache(GetCurrentProcess(), resizeSlot,
                                      sizeof(void *));
            }
        }
    }
}

bool writeWidgetSnapshot() {
    QFile output(dllDirectory() + QStringLiteral("/dpi_vtable_history.log"));
    if (!output.open(QIODevice::Append | QIODevice::Text))
        return false;
    QTextStream stream(&output);
    int count = 0;
    stream << "--- " << QDateTime::currentDateTime().toString(Qt::ISODate)
           << " metricIndex=" << g_metricIndex
           << " resizeGlCandidates=";
    for (int index : g_resizeGlCandidates)
        stream << index << ',';
    stream
           << " resizeGlIndex=" << kResizeGlIndex
           << " orthoResizeCalls=" << g_orthoResizeCalls
           << " lastOrthoInput=" << g_lastOrthoInputWidth << 'x'
           << g_lastOrthoInputHeight
           << " patchCount=" << g_patches.size() << " ---\n";
    for (QWidget *widget : QApplication::allWidgets()) {
        if (!widget)
            continue;
        const QString cls = QString::fromLatin1(widget->metaObject()->className());
        if (cls != QStringLiteral("MriCanvasWidget") &&
            cls != QStringLiteral("MriCanvasContainer") &&
            cls != QStringLiteral("MriProjectController") &&
            cls != QStringLiteral("MriProjectListWidget"))
            continue;
        stream << "class=" << cls
               << " ptr=0x" << QString::number(
                      reinterpret_cast<quintptr>(widget), 16)
               << " object=" << widget->objectName()
               << " size=" << widget->width() << 'x' << widget->height()
               << " dpr=" << widget->devicePixelRatioF()
               << " targetDpr=" << ratioForCanvas(widget)
               << " visible=" << widget->isVisible()
               << " QOpenGLWidget=" << widget->inherits("QOpenGLWidget")
               << " QGLWidget=" << widget->inherits("QGLWidget");
        if (QWidget *parent = widget->parentWidget()) {
            stream << " parent=" << parent->metaObject()->className()
                   << ':' << parent->objectName();
            if (QWidget *grandparent = parent->parentWidget())
                stream << " grandparent=" << grandparent->metaObject()->className()
                       << ':' << grandparent->objectName();
        }
        stream << '\n';
        ++count;
    }
    return count > 0;
}

void startExperiment(QApplication *app) {
    locateResizeGlCandidates();
    scanOpenGlWidgets();
    auto *timer = new QTimer(app);
    timer->setInterval(1000);
    QObject::connect(timer, &QTimer::timeout, [] { scanOpenGlWidgets(); });
    timer->start();
    auto *snapshotTimer = new QTimer(app);
    snapshotTimer->setInterval(2000);
    QObject::connect(snapshotTimer, &QTimer::timeout,
                     [] { writeWidgetSnapshot(); });
    snapshotTimer->start();
}

DWORD WINAPI worker(LPVOID) {
    QApplication *app = nullptr;
    for (int i = 0; i < 3000; ++i) {
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
