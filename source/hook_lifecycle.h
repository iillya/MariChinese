#pragma once

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QEvent>
#include <QtCore/QPointer>
#include <QtWidgets/QApplication>

#include <atomic>

// Shared lifecycle policy for hooks injected into Mari.
//
// 1. Wait for QApplication without touching Qt objects from DllMain.
// 2. Install hooks for objects/modules that already exist on the GUI thread.
// 3. Use Qt lifecycle events for objects created later.
// 4. Poll only for Mari components that can bypass or precede those events.
namespace MariHookLifecycle {

constexpr int kApplicationWaitAttempts = 300;
constexpr int kApplicationWaitIntervalMs = 100;
constexpr int kDeferredScanIntervalMs = 2000;
constexpr int kDeferredScanWindowMs = 60000;
// Phase 3 compatibility fallback. It is disabled by default and enabled by the
// launcher only when settings.ini contains [Hooks] FallbackPolling=1.
inline bool DeferredPollingEnabled() {
    wchar_t value[8] = {};
    return GetEnvironmentVariableW(L"MARI_CHINESE_FALLBACK_POLLING", value,
                                   static_cast<DWORD>(_countof(value))) > 0 &&
           value[0] == L'1';
}

using GuiInitializer = void (*)(QApplication *);

// DllMain publishes the unified hook's GUI initializer before creating the
// worker thread.
inline std::atomic<GuiInitializer> g_guiInitializer{nullptr};

class GuiInitializationReceiver final : public QObject {
public:
    GuiInitializationReceiver(QApplication *application, GuiInitializer initializer)
        : application_(application), initializer_(initializer) {
        connect(application, &QObject::destroyed, this, &QObject::deleteLater);
    }

protected:
    bool event(QEvent *event) override {
        if (event->type() != QEvent::User) return QObject::event(event);
        const QPointer<GuiInitializationReceiver> guard(this);
        if (application_) {
            setParent(application_);
            initializer_(application_);
        }
        if (guard) guard->deleteLater();
        return true;
    }

private:
    QPointer<QApplication> application_;
    GuiInitializer initializer_;
};

inline DWORD WINAPI InitializationWorker(LPVOID) {
    // The hook is process-lifetime: installed IAT/vtable entries and Qt
    // callbacks cannot survive unloading their implementation.
    HMODULE pinned = nullptr;
    if (!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                           GET_MODULE_HANDLE_EX_FLAG_PIN,
                           reinterpret_cast<LPCWSTR>(&InitializationWorker), &pinned))
        return 1;
    QApplication *application = nullptr;
    for (int attempt = 0; attempt < kApplicationWaitAttempts; ++attempt) {
        if (QCoreApplication *core = QCoreApplication::instance()) {
            application = qobject_cast<QApplication *>(core);
            if (application)
                break;
        }
        Sleep(kApplicationWaitIntervalMs);
    }

    const GuiInitializer initializer =
        g_guiInitializer.load(std::memory_order_acquire);
    if (!application || !initializer)
        return 1;

    // Qt 5.6's singleShot(functor) can lose the callback when its originating
    // native worker has no event loop. postEvent targets the GUI queue directly
    // and works before or after QApplication::exec starts.
    auto *receiver = new GuiInitializationReceiver(application, initializer);
    receiver->moveToThread(application->thread());
    QCoreApplication::postEvent(receiver, new QEvent(QEvent::User));
    return 0;
}

// The only lifecycle operation allowed from DllMain. No Qt object is accessed
// here; the worker performs the wait and GUI-thread handoff after loader-lock
// processing has returned.
inline bool StartGuiInitialization(GuiInitializer initializer) {
    if (!initializer)
        return false;
    g_guiInitializer.store(initializer, std::memory_order_release);
    HANDLE thread = CreateThread(nullptr, 0, InitializationWorker,
                                 nullptr, 0, nullptr);
    if (!thread)
        return false;
    CloseHandle(thread);
    return true;
}

} // namespace MariHookLifecycle
