// Mari OpenGL high-DPI compatibility hook. This DLL contains no localization.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QAbstractNativeEventFilter>
#include <QtCore/QEvent>
#include <QtCore/QPointer>
#include <QtCore/QTimer>
#include <QtGui/QResizeEvent>
#include <QtWidgets/QApplication>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QWidget>

#include <vector>

#include "hook_lifecycle.h"
#include "dpi_hook.h"

namespace {

using PaintDeviceMetricFn = int (__cdecl *)(const QPaintDevice *, int);

struct CanvasPatch {
    void **vtable = nullptr;
    PaintDeviceMetricFn originalMetric = nullptr;
};

constexpr qreal kCanvasDevicePixelRatio = 1.0;

SRWLOCK g_patchLock = SRWLOCK_INIT;
std::vector<CanvasPatch> g_canvasPatches;

struct VtableLayout {
    int metricIndex = -1;
};

VtableLayout g_modernLayout;
VtableLayout g_legacyLayout;

// QWidget uses multiple inheritance (QObject + QPaintDevice). Calls made
// through QPaintDevice::devicePixelRatioF() dispatch through the QPaintDevice
// subobject's vptr, which is not guaranteed to be QWidget's primary vptr.
// MriImageViewWidget exercises that secondary path, while Mari's main canvas
// happens to dispatch through the primary table. Always address the actual
// QPaintDevice subobject so both paths agree.
const QPaintDevice *paintDeviceFor(const QWidget *widget) {
    return widget ? static_cast<const QPaintDevice *>(widget) : nullptr;
}

void **paintDeviceVtable(const QPaintDevice *device) {
    if (!device)
        return nullptr;
    return *reinterpret_cast<void ***>(const_cast<QPaintDevice *>(device));
}

void **paintDeviceVtable(const QWidget *widget) {
    return paintDeviceVtable(paintDeviceFor(widget));
}

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
                    VtableLayout &layout) {
    if (!baseVtable || !metricAddress || layout.metricIndex >= 0)
        return;
    for (int index = 0; index < 128; ++index) {
        if (baseVtable[index] == metricAddress) {
            layout.metricIndex = index;
            break;
        }
    }
}

void discoverVtableLayouts() {
    // Build the modern QOpenGLWidget probe (and resolve the metric slot) only
    // once. This function is exercised from isMetricHookLive() on
    // every lifecycle/paint/resize event for GL surfaces; constructing a
    // QOpenGLWidget on the stack each time would needlessly churn the GUI thread.
    static bool discovered = false;
    if (discovered)
        return;
    discovered = true;
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!qtWidgets) return;

    // Modern QOpenGLWidget lives in Qt5Widgets, so its vtable layout can be
    // discovered statically. Legacy QGLWidget (Qt5OpenGL) cannot: the shared Qt
    // SDK ships only Qt5Core/Gui/Widgets, and Qt5OpenGL is only guaranteed to be
    // loaded once a real QGLWidget exists, so its layout is discovered lazily in
    // discoverLegacyLayout() below.
    QOpenGLWidget modernProbe;
    void **modernVtable = paintDeviceVtable(&modernProbe);
    discoverLayout(
        modernVtable,
        reinterpret_cast<void *>(GetProcAddress(qtWidgets,
            "?metric@QOpenGLWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z")),
        g_modernLayout);
}

// Lazily discover the legacy QGLWidget vtable layout from a real widget. Qt5OpenGL
// is loaded only while such a widget exists, so GetModuleHandle/GetProcAddress
// only succeed here; this keeps the DLL free of any compile/link dependency on
// Qt5OpenGL (the shared SDK omits that module).
void discoverLegacyLayout(const QWidget *widget) {
    if (!widget || !widget->inherits("QGLWidget"))
        return;
    if (g_legacyLayout.metricIndex >= 0)
        return;
    void **vtable = paintDeviceVtable(widget);
    HMODULE qtOpenGl = GetModuleHandleW(L"Qt5OpenGL.dll");
    HMODULE qtWidgets = GetModuleHandleW(L"Qt5Widgets.dll");
    if (!qtOpenGl || !qtWidgets)
        return;
    discoverLayout(
        vtable,
        reinterpret_cast<void *>(GetProcAddress(qtWidgets,
            "?metric@QWidget@@MEBAHW4PaintDeviceMetric@QPaintDevice@@@Z")),
        g_legacyLayout);
}

const VtableLayout *layoutFor(const QWidget *widget) {
    if (widget && widget->inherits("QOpenGLWidget"))
        return &g_modernLayout;
    if (widget && widget->inherits("QGLWidget")) {
        discoverLegacyLayout(widget);
        return g_legacyLayout.metricIndex >= 0 ? &g_legacyLayout : nullptr;
    }
    return nullptr;
}

PaintDeviceMetricFn originalMetricFor(const QPaintDevice *device) {
    void **vtable = paintDeviceVtable(device);
    AcquireSRWLockShared(&g_patchLock);
    PaintDeviceMetricFn result = nullptr;
    for (const CanvasPatch &patch : g_canvasPatches) {
        if (patch.vtable == vtable) {
            result = patch.originalMetric;
            break;
        }
    }
    ReleaseSRWLockShared(&g_patchLock);
    return result;
}

int hookedMetric(const QPaintDevice *self, int metric) {
    const auto kind = static_cast<QPaintDevice::PaintDeviceMetric>(metric);
    if (kind == QPaintDevice::PdmDevicePixelRatio)
        return static_cast<int>(kCanvasDevicePixelRatio);
    if (kind == QPaintDevice::PdmDevicePixelRatioScaled) {
        return static_cast<int>(kCanvasDevicePixelRatio *
                                QPaintDevice::devicePixelRatioFScale());
    }
    const PaintDeviceMetricFn original = originalMetricFor(self);
    return original ? original(self, metric) : 1;
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

bool patchCanvas(QWidget *widget) {
    if (!widget || !isOpenGlSurface(widget))
        return false;
    discoverVtableLayouts();
    const VtableLayout *layout = layoutFor(widget);
    if (!layout || layout->metricIndex < 0)
        return false;

    void **vtable = paintDeviceVtable(widget);
    if (!vtable)
        return false;

    AcquireSRWLockExclusive(&g_patchLock);
    for (const CanvasPatch &patch : g_canvasPatches) {
        if (patch.vtable == vtable) {
            const bool live = vtable[layout->metricIndex] ==
                reinterpret_cast<void *>(&hookedMetric);
            const bool repaired = live || replaceVtableSlot(
                &vtable[layout->metricIndex],
                reinterpret_cast<void *>(&hookedMetric));
            ReleaseSRWLockExclusive(&g_patchLock);
            return repaired;
        }
    }

    void **metricSlot = &vtable[layout->metricIndex];
    const auto originalMetric = reinterpret_cast<PaintDeviceMetricFn>(*metricSlot);
    if (!isExecutableAddress(reinterpret_cast<void *>(originalMetric))) {
        ReleaseSRWLockExclusive(&g_patchLock);
        return false;
    }

    g_canvasPatches.push_back({vtable, originalMetric});
    const bool metricPatched = replaceVtableSlot(
        metricSlot, reinterpret_cast<void *>(&hookedMetric));
    if (!metricPatched)
        g_canvasPatches.pop_back();
    ReleaseSRWLockExclusive(&g_patchLock);
    return metricPatched;
}

// Forward-declared: verify whether the live metric() slot is our replacement.
// Defined after observeWidget, which calls it, to keep the readability of that
// function with the patch-checking helper it depends on.
bool isMetricHookLive(const QWidget *widget);

void observeWidget(QWidget *widget) {
    if (!widget)
        return;
    if (!isOpenGlSurface(widget))
        return;
    // A surface can first be observed while its vptr still references a base
    // class during construction. Verify the live slot rather than caching the
    // widget pointer; the most-derived constructor may replace that vptr later.
    if (isMetricHookLive(widget))
        return;
    if (!patchCanvas(widget))
        return;
    // A late-created QOpenGLWidget may already own an FBO sized with Qt's scaled
    // DPR. Re-deliver its current size after the override is live so Qt recreates
    // that FBO using DPR 1.0, then request a repaint. Repeating this on every
    // pass is harmless: once the slot is live the function returns above.
    const QPointer<QWidget> widgetGuard(widget);
    QTimer::singleShot(0, widget, [widgetGuard] {
        if (!widgetGuard) return;
        const QSize size = widgetGuard->size();
        QResizeEvent resizeEvent(size, size);
        QApplication::sendEvent(widgetGuard, &resizeEvent);
        widgetGuard->update();
    });
}

// Return true only when the widget's live metric() slot is genuinely our
// replacement. A base-class vtable patched during construction can be replaced
// by the derived-class vtable before the widget is shown, so cached object state
// is not sufficient.
bool isMetricHookLive(const QWidget *widget) {
    if (!widget)
        return false;
    discoverVtableLayouts();
    const VtableLayout *layout = layoutFor(widget);
    if (!layout || layout->metricIndex < 0)
        return false;
    void **vtable = paintDeviceVtable(widget);
    if (!vtable)
        return false;
    return vtable[layout->metricIndex] ==
           reinterpret_cast<void *>(&hookedMetric);
}

// Defer a complete scan until the current window-creation / lifecycle event has
// returned. This is the safe place to inspect freshly created OpenGL surfaces
// whose native window / vtable is not final during the construction event.
void scheduleDeferredScan() {
    static bool scanScheduled = false;
    if (scanScheduled)
        return;
    scanScheduled = true;
    QTimer::singleShot(0, QApplication::instance(), [] {
        scanScheduled = false;
        for (QWidget *widget : QApplication::allWidgets())
            observeWidget(widget);
    });
}

class WidgetLifecycleFilter final : public QObject {
public:
    using QObject::QObject;

    bool eventFilter(QObject *object, QEvent *event) override {
        const QEvent::Type type = event->type();
        bool deferredScan = false;
        // A GL surface's native window may be created / exposed at Create or
        // WinIdChange even when the control never emits Polish/Show (e.g. some
        // Mari image viewers). Observe there too so the patch lands on the
        // newly created OpenGL surface.
        switch (type) {
            case QEvent::Polish:
            case QEvent::Show:
            case QEvent::Create:
            case QEvent::WinIdChange:
                if (auto *widget = qobject_cast<QWidget *>(object)) {
                    observeWidget(widget);
                    // Showing an ordinary menu/control is common and does not
                    // justify a full allWidgets() pass. A top-level window can
                    // contain a GL child that never receives Show itself.
                    if (type != QEvent::Show || widget->isWindow())
                        deferredScan = true;
                }
                break;
            case QEvent::ChildAdded:
                // The child is not guaranteed to be fully constructed yet.
                // The deferred scan below observes it on the next event turn.
                deferredScan = true;
                break;
            default:
                break;
        }
        // A containing dialog can show without the GL child emitting Show, and a
        // brand-new native window can bypass Polish/Show entirely. Run a deferred
        // scan on every window-creation / lifecycle trigger, not only Show.
        if (type == QEvent::WindowActivate)
            deferredScan = true;
        if (deferredScan)
            scheduleDeferredScan();
        return false;
    }
};

// Listen at the Windows message layer for native window creation. Mari can
// create an OpenGL HWND that never triggers the Qt lifecycle events above (its
// main viewport is a native WGL window). On WM_CREATE we only schedule a
// deferred scan: at that instant the QWidget may not be registered with its
// HWND yet, but by the next event-loop tick it is.
class NativeWindowCreationFilter final : public QAbstractNativeEventFilter {
public:
    bool nativeEventFilter(const QByteArray &eventType, void *message,
                           long *result) override {
        Q_UNUSED(result);
        if (eventType == "windows_generic_MSG") {
            const MSG *msg = static_cast<const MSG *>(message);
            if (msg && msg->message == WM_CREATE)
                scheduleDeferredScan();
        }
        return false;
    }
};

void initializeDpiOnGuiThread(QApplication *app) {
    // Phase 1: patch all OpenGL widgets that already exist.
    discoverVtableLayouts();
    // Phase 2: keep the event filter installed for widgets created later.
    app->installEventFilter(new WidgetLifecycleFilter(app));
    // Also listen for native window creation, which can bypass the Qt lifecycle
    // events above (Mari's main viewport is a native WGL surface).
    app->installNativeEventFilter(new NativeWindowCreationFilter);
    for (QWidget *widget : QApplication::allWidgets())
        observeWidget(widget);

    // Optional compatibility fallback for Mari versions or plug-ins that bypass
    // all lifecycle/native-window events. Disabled by default.
    if (!MariHookLifecycle::DeferredPollingEnabled())
        return;

    auto *snapshotTimer = new QTimer(app);
    snapshotTimer->setInterval(MariHookLifecycle::kDeferredScanIntervalMs);
    QObject::connect(snapshotTimer, &QTimer::timeout, snapshotTimer,
                     [] {
                         for (QWidget *widget : QApplication::allWidgets())
                             observeWidget(widget);
                     });
    snapshotTimer->start();
}

} // namespace

namespace MariDpiHook {

bool Enabled() {
    wchar_t value[8] = {};
    return GetEnvironmentVariableW(L"MARI_CHINESE_DPI_ENABLED", value,
                                   static_cast<DWORD>(_countof(value))) > 0 &&
           value[0] == L'1';
}

void Initialize(QApplication *application) {
    if (application && Enabled())
        initializeDpiOnGuiThread(application);
}

} // namespace MariDpiHook
