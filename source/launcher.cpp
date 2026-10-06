// ============================================================================
//  Mari 中文汉化 - 启动器
// ============================================================================
//  Mari 没有插件入口，所以这个启动器（与 Toolbag / SpeedTree 汉化器一致）
//  启动已安装的 Mari，等 Qt5Widgets 就绪后用远端 LoadLibraryW 线程注入
//  MariChineseHook.dll。汉化和可选的 4K 视口修复由同一 DLL 初始化。
//  采用普通启动而非挂起启动：挂起启动 + 提前注入汉化会改变 Qt 对 GL 画布
//  的生命周期，导致画布 resizeGL 不被调用，4K 下画布缩小。原程序文件从不
//  修改；命令行参数（例如 .mri 项目路径）原样透传给 Mari。
// ============================================================================

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>
#include <cmath>
#include <cwchar>
#include <string>
#include <utility>
#include <vector>

#include "qt_compatibility.h"

namespace {

std::wstring ParentDir(const std::wstring &path) {
    size_t slash = path.find_last_of(L"\\/");
    return slash == std::wstring::npos ? L"" : path.substr(0, slash);
}

bool IsFile(const std::wstring &path) {
    DWORD attr = GetFileAttributesW(path.c_str());
    return attr != INVALID_FILE_ATTRIBUTES && !(attr & FILE_ATTRIBUTE_DIRECTORY);
}

std::wstring ExePath() {
    std::vector<wchar_t> buf(1024);
    while (buf.size() <= 32768) {
        DWORD n = GetModuleFileNameW(nullptr, buf.data(), (DWORD)buf.size());
        if (!n) return L"";
        if (n < buf.size() - 1) return std::wstring(buf.data(), n);
        buf.resize(buf.size() * 2);
    }
    return L"";
}

std::wstring FindMariExeInDir(const std::wstring &dir) {
    WIN32_FIND_DATAW data{};
    HANDLE find = FindFirstFileW((dir + L"\\Mari*.exe").c_str(), &data);
    if (find == INVALID_HANDLE_VALUE)
        return L"";
    std::wstring result;
    do {
        const std::wstring name = data.cFileName;
        // Mari version executables are named Mari<digit>..., which excludes
        // this launcher and helper executables.
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
            name.size() > 4 && name[4] >= L'0' && name[4] <= L'9') {
            result = dir + L"\\" + name;
            break;
        }
    } while (FindNextFileW(find, &data));
    FindClose(find);
    return result;
}

std::wstring FindMariUnderProgramFiles(const std::wstring &programFiles) {
    WIN32_FIND_DATAW data{};
    HANDLE find = FindFirstFileW((programFiles + L"\\Mari*").c_str(), &data);
    if (find == INVALID_HANDLE_VALUE)
        return L"";
    std::wstring result;
    do {
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
            wcscmp(data.cFileName, L".") == 0 || wcscmp(data.cFileName, L"..") == 0)
            continue;
        const std::wstring candidate = programFiles + L"\\" + data.cFileName +
                                       L"\\Bundle\\bin";
        const std::wstring found = FindMariExeInDir(candidate);
        if (!found.empty() && MariQtCompatibility::isAmd64Image(found) &&
            MariQtCompatibility::supportedDirectory(candidate) &&
            (result.empty() || _wcsicmp(found.c_str(), result.c_str()) > 0))
            result = found;
    } while (FindNextFileW(find, &data));
    FindClose(find);
    return result;
}

// 优先从启动器位置向上查找；仅在安装目录损坏或启动器被单独移动时，
// 才枚举 Program Files 下所有 Mari 安装，不依赖具体 Mari 版本号。
std::wstring FindMariExe(const std::wstring &start) {
    std::wstring dir = start;
    for (int depth = 0; depth < 12; ++depth) {
        const std::wstring found = FindMariExeInDir(dir);
        if (!found.empty() && MariQtCompatibility::isAmd64Image(found) &&
            MariQtCompatibility::supportedDirectory(ParentDir(found))) return found;
        std::wstring parent = ParentDir(dir);
        if (parent.empty() || parent == dir) break;
        dir = parent;
    }
    wchar_t pf[MAX_PATH] = {};
    DWORD pfLen = GetEnvironmentVariableW(L"ProgramFiles", pf, MAX_PATH);
    if (pfLen == 0 || pfLen >= MAX_PATH)
        pfLen = GetEnvironmentVariableW(L"ProgramW6432", pf, MAX_PATH);
    if (pfLen && pfLen < MAX_PATH) {
        return FindMariUnderProgramFiles(pf);
    }
    return L"";
}

bool SameArchitecture(HANDLE targetProcess) {
    using IsWow64Process2Fn = BOOL (WINAPI *)(HANDLE, USHORT *, USHORT *);
    const auto isWow64Process2 = reinterpret_cast<IsWow64Process2Fn>(
        GetProcAddress(GetModuleHandleW(L"kernel32.dll"), "IsWow64Process2"));
    if (isWow64Process2) {
        USHORT localProcess = 0, localNative = 0;
        USHORT remoteProcess = 0, remoteNative = 0;
        if (!isWow64Process2(GetCurrentProcess(), &localProcess, &localNative) ||
            !isWow64Process2(targetProcess, &remoteProcess, &remoteNative))
            return false;
        const USHORT localMachine = localProcess ? localProcess : localNative;
        const USHORT remoteMachine = remoteProcess ? remoteProcess : remoteNative;
        return localMachine == remoteMachine;
    }
    BOOL localWow64 = FALSE, remoteWow64 = FALSE;
    return IsWow64Process(GetCurrentProcess(), &localWow64) &&
           IsWow64Process(targetProcess, &remoteWow64) &&
           localWow64 == remoteWow64;
}

LPTHREAD_START_ROUTINE ResolveLoadLibrary(HANDLE targetProcess, DWORD pid) {
    if (!SameArchitecture(targetProcess)) return nullptr;
    HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    FARPROC fn = kernel32 ? GetProcAddress(kernel32, "LoadLibraryW") : nullptr;
    if (!fn) return nullptr;
    // LoadLibraryW can be forwarded to KernelBase. Resolve its containing
    // module in both processes instead of assuming identical ASLR addresses.
    HMODULE localModule = nullptr;
    if (!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                            GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                            reinterpret_cast<LPCWSTR>(fn), &localModule))
        return nullptr;
    wchar_t localPath[MAX_PATH] = {};
    const DWORD localPathLength = GetModuleFileNameW(localModule, localPath, MAX_PATH);
    if (!localPathLength || localPathLength >= MAX_PATH) return nullptr;
    const wchar_t *name = wcsrchr(localPath, L'\\');
    name = name ? name + 1 : localPath;
    const auto offset = reinterpret_cast<const BYTE *>(fn) -
                        reinterpret_cast<const BYTE *>(localModule);
    HANDLE snapshot = CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
    if (snapshot == INVALID_HANDLE_VALUE) return nullptr;
    LPTHREAD_START_ROUTINE remote = nullptr;
    MODULEENTRY32W module{};
    module.dwSize = sizeof(module);
    if (Module32FirstW(snapshot, &module)) {
        do {
            if (_wcsicmp(module.szModule, name) == 0 &&
                offset < module.modBaseSize) {
                remote = reinterpret_cast<LPTHREAD_START_ROUTINE>(
                    module.modBaseAddr + offset);
                break;
            }
        } while (Module32NextW(snapshot, &module));
    }
    CloseHandle(snapshot);
    return remote;
}

bool WaitForModule(DWORD pid, const wchar_t *moduleName, DWORD timeoutMs) {
    const bool fullPath = wcschr(moduleName, L'\\') || wcschr(moduleName, L'/');
    const ULONGLONG started = GetTickCount64();
    do {
        HANDLE snapshot = CreateToolhelp32Snapshot(
            TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
        if (snapshot != INVALID_HANDLE_VALUE) {
            MODULEENTRY32W module{};
            module.dwSize = sizeof(module);
            if (Module32FirstW(snapshot, &module)) {
                do {
                    if (_wcsicmp(fullPath ? module.szExePath : module.szModule,
                                 moduleName) == 0) {
                        CloseHandle(snapshot);
                        return true;
                    }
                } while (Module32NextW(snapshot, &module));
            }
            CloseHandle(snapshot);
        }
        if (!timeoutMs || GetTickCount64() - started >= timeoutMs) break;
        Sleep(100);
    } while (true);
    return false;
}

bool HasMariWindow(DWORD pid) {
    struct Search { DWORD pid; bool found; } search{pid, false};
    EnumWindows([](HWND window, LPARAM context) -> BOOL {
        auto *state = reinterpret_cast<Search *>(context);
        DWORD owner = 0;
        GetWindowThreadProcessId(window, &owner);
        if (owner != state->pid || !IsWindowVisible(window)) return TRUE;
        wchar_t className[128]{};
        GetClassNameW(window, className, _countof(className));
        if (wcsncmp(className, L"Qt", 2) == 0) {
            state->found = true;
            return FALSE;
        }
        return TRUE;
    }, reinterpret_cast<LPARAM>(&search));
    return search.found;
}

// A closing translated Mari instance can outlive its main window. Avoid
// starting the next project while that exact host image is still tearing down.
bool WaitForExistingMariTransition(const std::wstring &exePath,
                                   const std::wstring &dllPath,
                                   DWORD timeoutMs) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) return true;
    std::vector<std::pair<DWORD, HANDLE>> pending;
    const std::wstring imageName = exePath.substr(exePath.find_last_of(L"\\/") + 1);
    PROCESSENTRY32W entry{};
    entry.dwSize = sizeof(entry);
    if (Process32FirstW(snapshot, &entry)) {
        do {
            if (entry.th32ProcessID == GetCurrentProcessId() ||
                _wcsicmp(entry.szExeFile, imageName.c_str()) != 0) continue;
            HANDLE process = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
                                         FALSE, entry.th32ProcessID);
            if (!process) continue;
            std::vector<wchar_t> image(32768);
            DWORD length = static_cast<DWORD>(image.size());
            const bool sameImage = QueryFullProcessImageNameW(process, 0, image.data(), &length) &&
                                   _wcsicmp(std::wstring(image.data(), length).c_str(),
                                            exePath.c_str()) == 0;
            if (sameImage && WaitForSingleObject(process, 0) == WAIT_TIMEOUT &&
                WaitForModule(entry.th32ProcessID, dllPath.c_str(), 0) &&
                !HasMariWindow(entry.th32ProcessID)) {
                pending.emplace_back(entry.th32ProcessID, process);
            } else {
                CloseHandle(process);
            }
        } while (Process32NextW(snapshot, &entry));
    }
    CloseHandle(snapshot);
    const ULONGLONG deadline = GetTickCount64() + timeoutMs;
    bool ready = true;
    for (const auto &old : pending) {
        while (WaitForSingleObject(old.second, 0) == WAIT_TIMEOUT &&
               !HasMariWindow(old.first)) {
            if (GetTickCount64() >= deadline) { ready = false; break; }
            Sleep(100);
        }
        if (!ready) break;
    }
    for (const auto &old : pending) CloseHandle(old.second);
    return ready;
}

enum class QtReadiness { Ready, ProcessExited, TimedOut, WaitFailed };

QtReadiness WaitForMariQt(HANDLE process, DWORD pid, DWORD timeoutMs) {
    const ULONGLONG deadline = GetTickCount64() + timeoutMs;
    for (;;) {
        const DWORD status = WaitForSingleObject(process, 0);
        if (status == WAIT_OBJECT_0) return QtReadiness::ProcessExited;
        if (status != WAIT_TIMEOUT) return QtReadiness::WaitFailed;
        if (WaitForModule(pid, L"Qt5Widgets.dll", 0)) return QtReadiness::Ready;
        const ULONGLONG now = GetTickCount64();
        if (now >= deadline) return QtReadiness::TimedOut;
        const DWORD remaining = static_cast<DWORD>(deadline - now < 100 ? deadline - now : 100);
        const DWORD waited = WaitForSingleObject(process, remaining);
        if (waited == WAIT_OBJECT_0) return QtReadiness::ProcessExited;
        if (waited != WAIT_TIMEOUT) return QtReadiness::WaitFailed;
    }
}

bool InjectDll(HANDLE process, DWORD pid, const std::wstring &path) {
    const SIZE_T bytes = (path.size() + 1) * sizeof(wchar_t);
    void *remote = VirtualAllocEx(process, nullptr, bytes,
                                  MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    SIZE_T written = 0;
    if (!remote || !WriteProcessMemory(process, remote, path.c_str(), bytes,
                                        &written) || written != bytes) {
        if (remote) VirtualFreeEx(process, remote, 0, MEM_RELEASE);
        return false;
    }
    const auto loadLibrary = ResolveLoadLibrary(process, pid);
    HANDLE thread = loadLibrary ? CreateRemoteThread(
        process, nullptr, 0, loadLibrary, remote, 0, nullptr) : nullptr;
    bool loaded = false;
    if (thread) {
        const DWORD wait = WaitForSingleObject(thread, 30000);
        // A remote thread's exit code is DWORD-sized and cannot reliably carry
        // a 64-bit HMODULE. Verify the target module list instead.
        loaded = wait == WAIT_OBJECT_0 && WaitForModule(pid, path.c_str(), 2000);
        // The target thread can still be reading this buffer after a timeout.
        // Leave the small allocation to the target process in that case.
        if (wait == WAIT_OBJECT_0)
            VirtualFreeEx(process, remote, 0, MEM_RELEASE);
        CloseHandle(thread);
    } else {
        VirtualFreeEx(process, remote, 0, MEM_RELEASE);
    }
    return loaded;
}

void ConfigureDpi(const std::wstring &directory) {
    const std::wstring settings = directory + L"\\settings.ini";
    const int enabled = GetPrivateProfileIntW(L"Dpi", L"Enabled", 0,
                                               settings.c_str());
    SetEnvironmentVariableW(L"MARI_CHINESE_DPI_ENABLED",
                            enabled ? L"1" : L"0");
    if (!enabled)
        return;

    wchar_t value[32] = L"1.75";
    GetPrivateProfileStringW(L"Dpi", L"ScaleFactor", L"1.75", value,
                             static_cast<DWORD>(_countof(value)),
                             settings.c_str());
    wchar_t *end = nullptr;
    const double factor = std::wcstod(value, &end);
    if (end == value || *end != L'\0' || !std::isfinite(factor) ||
        factor < 1.0 || factor > 3.0) {
        wcscpy_s(value, L"1.75");
    }
    SetEnvironmentVariableW(L"QT_ENABLE_HIGHDPI_SCALING", L"1");
    SetEnvironmentVariableW(L"QT_AUTO_SCREEN_SCALE_FACTOR", L"1");
    SetEnvironmentVariableW(L"QT_SCALE_FACTOR", value);
}

void ConfigureHookLifecycle(const std::wstring &directory) {
    const std::wstring settings = directory + L"\\settings.ini";
    const int enabled = GetPrivateProfileIntW(L"Hooks", L"FallbackPolling", 0,
                                               settings.c_str());
    SetEnvironmentVariableW(L"MARI_CHINESE_FALLBACK_POLLING",
                            enabled ? L"1" : L"0");
}

} // namespace

int APIENTRY wWinMain(HINSTANCE, HINSTANCE, PWSTR cmdLine, int) {
    const std::wstring own = ExePath();
    const std::wstring dir = ParentDir(own);
    const std::wstring exePath = FindMariExe(dir);
    const std::wstring root = ParentDir(exePath);
    const std::wstring dllPath = dir + L"\\MariChineseHook.dll";

    if (root.empty() || !IsFile(dllPath) || !IsFile(exePath)) {
        MessageBoxW(nullptr,
                    L"找不到受支持的 Mari 可执行文件或汉化 DLL。\n"
                    L"请重新运行安装程序，修复 ChineseLauncher 目录。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 1;
    }
    if (!MariQtCompatibility::supportedDirectory(root)) {
        MessageBoxW(nullptr,
                    L"Mari 的 Qt5 组件不完整或组件版本不一致。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 1;
    }

    ConfigureHookLifecycle(dir);
    ConfigureDpi(dir);

    if (!WaitForExistingMariTransition(exePath, dllPath, 30000)) {
        MessageBoxW(nullptr, L"上一个 Mari 进程仍在关闭。请稍后再打开工程。",
                    L"Mari 中文补丁", MB_OK | MB_ICONWARNING);
        return 3;
    }

    STARTUPINFOW si{}; si.cb = sizeof(si);
    PROCESS_INFORMATION pi{};
    std::wstring cl = L"\"" + exePath + L"\"";
    if (cmdLine && *cmdLine) { cl += L" "; cl += cmdLine; }
    std::vector<wchar_t> clBuf(cl.begin(), cl.end()); clBuf.push_back(L'\0');

    // 普通启动（不挂起）：Mari 进程即刻运行并加载 Qt。DPI 对照实验证明，
    // 挂起启动 + 先注入汉化会改变 Qt 对 GL 画布的生命周期（resizeGL 不再被
    // 调用），导致 4K 下画布缩小。改为等待 Qt 就绪后再注入，复现独立实验
    // 的成功路径。
    if (!CreateProcessW(exePath.c_str(), clBuf.data(), nullptr, nullptr, FALSE,
                        0, nullptr, root.c_str(), &si, &pi)) {
        MessageBoxW(nullptr, L"无法启动 Mari。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 2;
    }

    // 等待 Qt 就绪后再注入。汉化 DLL 自身的 worker 线程会在 QApplication
    // 出现后再初始化，因此 Qt 就绪后注入是安全的。
    const QtReadiness readiness = WaitForMariQt(pi.hProcess, pi.dwProcessId, 30000);
    bool ok = readiness == QtReadiness::Ready;
    if (readiness == QtReadiness::ProcessExited) {
        DWORD exitCode = 3;
        GetExitCodeProcess(pi.hProcess, &exitCode);
        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
        if (exitCode == 0) return 0; // Mari handed the project to an active instance.
        MessageBoxW(nullptr, L"Mari 在汉化加载前异常退出。请检查原版软件的启动日志。",
                    L"Mari 中文补丁", MB_OK | MB_ICONWARNING);
        return 3;
    }
    if (!ok) {
        MessageBoxW(nullptr,
                    readiness == QtReadiness::TimedOut
                        ? L"等待 Mari 的 Qt5Widgets.dll 超时。"
                        : L"等待 Mari 的 Qt5Widgets.dll 时发生错误。",
                    L"Mari 中文补丁", MB_OK | MB_ICONWARNING);
    }

    // 单次注入：DLL 在 GUI 线程依次初始化汉化和可选的 DPI 修复。
    if (ok) {
        ok = InjectDll(pi.hProcess, pi.dwProcessId, dllPath);
        if (!ok) {
            MessageBoxW(nullptr,
                        L"Mari 已启动，但汉化注入失败，将继续使用英文界面。",
                        L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        }
    }
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return ok ? 0 : 3;
}
