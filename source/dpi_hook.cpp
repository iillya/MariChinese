// Standalone Mari DPI experiment. This DLL contains no localization hooks.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QEvent>
#include <QtCore/QMetaObject>
#include <QtCore/QPointer>
#include <QtCore/QTimer>
#include <QtWidgets/QApplication>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QWidget>
#include <QtOpenGL/QGLWidget>

#include <vector>

#include "hook_lifecycle.h"

namespace {

using QWidgetMetricFn = int (__cdecl *)(const QWidget *, int);
using ResizeGlFn = void (__cdecl *)(QWidget *, int, int);

struct CanvasPatch {
    void **vtable = nullptr;
    QWidgetMetricFn originalMetric = nullptr;
    ResizeGlFn originalResizeGl = nullptr;
};

constexpr qreal kCanvasDevicePixelRatio = 1.0;

HINSTANCE g_instance = nullptr;
SRWLOCK g_patchLock = SRWLOCK_INIT;
std::vector<CanvasPatch> g_canvasPatches;
std::vector<QPointer<QWidget>> g_observedWidgets;

struct VtableLayout {
    int metricIndex = -1;
    int resizeGlIndex = -1;
};

VtableLayout g_modernLayout;
VtableLayout g_legacyLayout;

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

// Mari does not use OpenGL only for the main 3D canvas.  The colour picker,
// image/gradient previews and some plug-in panels also derive their rendering
// widgets from QOpenGLWidget.  Matching only MriCanvasWidget leaves those
// secondary surfaces with Qt's scaled device-pixel ratio and their framebuffer
// is consequently drawn into only part of the available widget.
//
// QObject::inherits() walks the Qt meta-object superclass chain, so this also
// covers Mari's private subclasses without depending on their version-specific
// class names. Do not broaden this to arbitrary QWidget subclasses: the
// vtable layouts below are discovered separately for QOpenGLWidget/QGLWidget.
bool isOpenGlSurface(const QWidget *widget) {
    return widget && (widget->inherits("QOpenGLWidget") ||
                      widget->inherits("QGLWidget"));
}

void discoverLayout(void **baseVtable, void *metricAddress,
                    void *resizeAddress, VtableLayout &layout) {
    if (!baseVtable || !metricAddress || !resizeAddress ||
        (layout.metricIndex >= 0 && layout.resizeGlIndex >= 0))
        return;
    std::vector<int> resizeCandidates;
    for (int index = 0; index < 128; ++index) {
        if (layout.metricIndex < 0 && baseVtable[index] == metricAddress)
            layout.metricIndex = index;
        if (baseVtable[index] == resizeAddress)
            resizeCandidates.push_back(index);
    }
    // MSVC may fold initializeGL(), resizeGL() and paintGL() to one address.
    // When that happens they form a three-slot run and resizeGL is the middle.
    for (std::size_t first = 0; first < resizeCandidates.size();) {
        std::size_t last = first;
        while (last + 1 < resizeCandidates.size() &&
               resizeCandidates[last + 1] == resizeCandidates[last] + 1)
            ++last;
        if (last - first + 1 == 3) {
            layout.resizeGlIndex = resizeCandidates[first + 1];
            break;
        }
        if (last == first) {
            layout.resizeGlIndex = resizeCandidates[first];
            break;
        }
        first = last + 1;
    }
}

void discoverVtableLayouts() {
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!qtWidgets) return;

    QOpenGLWidget modernProbe;
    void **modernVtable = *reinterpret_cast<void ***>(&modernProbe);
    discoverLayout(
        modernVtable,
        reinterpret_cast<void *>(GetProcAddress(qtWidgets,
            "?metric@QOpenGLWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z")),
        reinterpret_cast<void *>(GetProcAddress(qtWidgets,
            "?resizeGL@QOpenGLWidget@@MEAAXHH@Z")),
        g_modernLayout);

    // Mari still uses legacy QGLWidget for some image viewers and previews.
    // Its metric() slot is inherited from QWidget, while resizeGL() belongs to
    // Qt5OpenGL, so it requires a separately discovered vtable layout.
    HMODULE qtOpenGl = GetModuleHandleW(L"Qt5OpenGL.dll");
    if (!qtOpenGl) return;
    QGLWidget legacyProbe;
    void **legacyVtable = *reinterpret_cast<void ***>(&legacyProbe);
    discoverLayout(
        legacyVtable,
        reinterpret_cast<void *>(GetProcAddress(qtWidgets,
            "?metric@QWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z")),
        reinterpret_cast<void *>(GetProcAddress(qtOpenGl,
            "?resizeGL@QGLWidget@@MEAAXHH@Z")),
        g_legacyLayout);
}

const VtableLayout *layoutFor(const QWidget *widget) {
    if (widget && widget->inherits("QOpenGLWidget"))
        return &g_modernLayout;
    if (widget && widget->inherits("QGLWidget"))
        return &g_legacyLayout;
    return nullptr;
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
    // resizeGL 不影响实际视口渲染分辨率，保持原始宽高透传。
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
    if (!widget)
        return;
    if (!isOpenGlSurface(widget))
        return;
    discoverVtableLayouts();
    const VtableLayout *layout = layoutFor(widget);
    if (!layout || layout->metricIndex < 0 || layout->resizeGlIndex < 0)
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

    void **metricSlot = &vtable[layout->metricIndex];
    void **resizeSlot = &vtable[layout->resizeGlIndex];
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
    if (!widget)
        return;
    if (!isOpenGlSurface(widget))
        return;
    for (const QPointer<QWidget> &known : g_observedWidgets) {
        if (known == widget)
            return;
    }
    g_observedWidgets.push_back(widget);
    patchCanvas(widget);
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

void startExperiment(QApplication *app) {
    // Phase 1: patch all OpenGL widgets that already exist.
    discoverVtableLayouts();
    // Phase 2: keep the event filter installed for widgets created later.
    app->installEventFilter(new WidgetLifecycleFilter(app));
    for (QWidget *widget : QApplication::allWidgets())
        observeWidget(widget);

    // Phase 3: bounded polling fallback for Mari's main canvas, which can
    // bypass the normal Polish/Show path. The timer stops as soon as a vtable
    // has been patched; later widget types remain covered by the event filter.
    if (!MariHookLifecycle::kEnableDeferredPolling)
        return;

    auto *snapshotTimer = new QTimer(app);
    snapshotTimer->setInterval(MariHookLifecycle::kDeferredScanIntervalMs);
    QObject::connect(snapshotTimer, &QTimer::timeout, snapshotTimer,
                     [snapshotTimer] {
                         // 主动轮询扫描：发现并修补 OpenGL 控件。Mari 的主
                         // 画布可能不走 Qt 的 Polish/Show 事件，必须靠周期
                         // 扫描捕获。后续出现的颜色选择器、预览器等不同派生
                         // 类型由常驻的 WidgetLifecycleFilter 继续按虚表修补。
                         AcquireSRWLockShared(&g_patchLock);
                         const bool patched = !g_canvasPatches.empty();
                         ReleaseSRWLockShared(&g_patchLock);
                         if (patched) {
                             snapshotTimer->stop();
                             snapshotTimer->deleteLater();
                             return;
                         }
                         for (QWidget *widget : QApplication::allWidgets())
                             observeWidget(widget);
                     });
    snapshotTimer->start();
    const QPointer<QTimer> snapshotTimerGuard(snapshotTimer);
    QTimer::singleShot(MariHookLifecycle::kDeferredScanWindowMs, app,
                       [snapshotTimerGuard] {
                           if (snapshotTimerGuard) {
                               snapshotTimerGuard->stop();
                               snapshotTimerGuard->deleteLater();
                           }
                       });
}

DWORD WINAPI worker(LPVOID) {
    QApplication *app = nullptr;
    for (int attempt = 0;
         attempt < MariHookLifecycle::kApplicationWaitAttempts; ++attempt) {
        if (QCoreApplication::instance()) {
            app = qobject_cast<QApplication *>(QCoreApplication::instance());
            if (app)
                break;
        }
        Sleep(MariHookLifecycle::kApplicationWaitIntervalMs);
    }
    if (!app)
        return 1;
    QMetaObject::invokeMethod(app, [app] { startExperiment(app); });
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
