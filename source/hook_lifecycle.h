#pragma once

// Shared lifecycle policy for hooks injected into Mari.
//
// 1. Wait for QApplication without touching Qt objects from DllMain.
// 2. Install hooks for objects/modules that already exist on the GUI thread.
// 3. Use Qt lifecycle events for objects created later.
// 4. Poll only for Mari components that can bypass or precede those events.
namespace MariHookLifecycle {

constexpr int kApplicationWaitAttempts = 3000;
constexpr int kApplicationWaitIntervalMs = 100;
constexpr int kDeferredScanIntervalMs = 2000;
constexpr int kDeferredScanWindowMs = 60000;
// Phase 3 compatibility fallback. Disabled by default because the initial
// GUI-thread installation and Qt lifecycle events cover normal Mari usage
// without periodic scanning. Set this to true only if a Mari version or plug-in
// loads modules/widgets late while also bypassing the relevant Qt events.
// The fallback implementation is intentionally retained below its call sites.
constexpr bool kEnableDeferredPolling = false;

} // namespace MariHookLifecycle
