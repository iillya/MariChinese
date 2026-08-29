#pragma once

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <QtCore/QCoreApplication>
#include <QtCore/QTimer>
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

inline DWORD WINAPI InitializationWorker(LPVOID) {
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

    // Qt 5.6 supports the context overload. The callback is therefore executed
    // on QApplication's GUI thread even though this worker is not a Qt thread.
    QTimer::singleShot(0, application, [application, initializer] {
        initializer(application);
    });
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
