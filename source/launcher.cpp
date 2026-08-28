// ============================================================================
//  Mari 中文汉化 - 启动器
// ============================================================================
//  Mari 没有插件入口，所以这个启动器（与 Toolbag / SpeedTree 汉化器一致）
//  以 SUSPENDED 状态启动已安装的 Mari，用远端 LoadLibraryW 线程注入
//  MariChineseHook.dll，然后恢复运行。原程序文件从不修改；命令行参数
//  （例如 .mri 项目路径）原样透传给 Mari。
// ============================================================================

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>
#include <cwchar>
#include <string>
#include <vector>

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
        if (!found.empty() && (result.empty() || _wcsicmp(found.c_str(), result.c_str()) > 0))
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
        if (!found.empty()) return found;
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
    HMODULE local = GetModuleHandleW(L"kernel32.dll");
    if (!local) return nullptr;
    FARPROC fn = GetProcAddress(local, "LoadLibraryW");
    if (!fn) return nullptr;
    uintptr_t rva = (uintptr_t)fn - (uintptr_t)local;
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
    if (snap != INVALID_HANDLE_VALUE) {
        MODULEENTRY32W mod{}; mod.dwSize = sizeof(mod);
        if (Module32FirstW(snap, &mod)) {
            do {
                if (_wcsicmp(mod.szModule, L"kernel32.dll") == 0) {
                    CloseHandle(snap);
                    return (LPTHREAD_START_ROUTINE)((uintptr_t)mod.modBaseAddr + rva);
                }
            } while (Module32NextW(snap, &mod));
        }
        CloseHandle(snap);
    }
    // A newly created suspended process can temporarily omit kernel32 from
    // Toolhelp's module list. Windows shares system-DLL mappings
    // for same-architecture processes in one boot session; retain the proven
    // compatibility path, but never use it across architectures.
    return SameArchitecture(targetProcess)
        ? reinterpret_cast<LPTHREAD_START_ROUTINE>(fn)
        : nullptr;
}

void ConfigureDpi(const std::wstring &directory) {
    const std::wstring settings = directory + L"\\settings.ini";
    const int enabled = GetPrivateProfileIntW(L"Dpi", L"Enabled", 0,
                                               settings.c_str());
    if (!enabled)
        return;

    wchar_t value[32] = L"1.75";
    GetPrivateProfileStringW(L"Dpi", L"ScaleFactor", L"1.75", value,
                             static_cast<DWORD>(_countof(value)),
                             settings.c_str());
    wchar_t *end = nullptr;
    const double factor = std::wcstod(value, &end);
    if (end == value || *end != L'\0' || factor < 1.0 || factor > 3.0) {
        wcscpy_s(value, L"1.75");
    }
    SetEnvironmentVariableW(L"QT_ENABLE_HIGHDPI_SCALING", L"1");
    SetEnvironmentVariableW(L"QT_AUTO_SCREEN_SCALE_FACTOR", L"1");
    SetEnvironmentVariableW(L"QT_SCALE_FACTOR", value);
    SetEnvironmentVariableW(L"MARI_CHINESE_DPI_SCALE", value);
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
                    L"请重新运行安装程序，修复 MariChineseLauncher 目录。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 1;
    }

    ConfigureDpi(dir);

    STARTUPINFOW si{}; si.cb = sizeof(si);
    PROCESS_INFORMATION pi{};
    std::wstring cl = L"\"" + exePath + L"\"";
    if (cmdLine && *cmdLine) { cl += L" "; cl += cmdLine; }
    std::vector<wchar_t> clBuf(cl.begin(), cl.end()); clBuf.push_back(L'\0');

    if (!CreateProcessW(exePath.c_str(), clBuf.data(), nullptr, nullptr, FALSE,
                        CREATE_SUSPENDED, nullptr, root.c_str(), &si, &pi)) {
        MessageBoxW(nullptr, L"无法启动 Mari。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 2;
    }

    size_t bytes = (dllPath.size() + 1) * sizeof(wchar_t);
    void *remote = VirtualAllocEx(pi.hProcess, nullptr, bytes,
                                  MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    SIZE_T written = 0;
    bool pathOk = remote &&
        WriteProcessMemory(pi.hProcess, remote, dllPath.c_str(), bytes, &written) &&
        written == bytes;

    auto loadLib = ResolveLoadLibrary(pi.hProcess, pi.dwProcessId);
    HANDLE thread = nullptr;
    if (pathOk && loadLib)
        thread = CreateRemoteThread(pi.hProcess, nullptr, 0, loadLib, remote, 0, nullptr);

    bool ok = false;
    bool remoteThreadCompleted = false;
    if (thread) {
        DWORD wait = WaitForSingleObject(thread, 30000);
        remoteThreadCompleted = wait == WAIT_OBJECT_0;
        DWORD loadResult = 0;
        const bool loaded = wait == WAIT_OBJECT_0 &&
                            GetExitCodeThread(thread, &loadResult) &&
                            loadResult != 0;
        CloseHandle(thread);
        ok = loaded;
    }

    if (ok && ResumeThread(pi.hThread) != (DWORD)-1) {
        ok = true;
    } else {
        ok = false;
        TerminateProcess(pi.hProcess, 3);
        WaitForSingleObject(pi.hProcess, 5000);
        MessageBoxW(nullptr, L"汉化注入失败，已终止 Mari（原文件未受影响）。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
    }

    if (remote && remoteThreadCompleted)
        VirtualFreeEx(pi.hProcess, remote, 0, MEM_RELEASE);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return ok ? 0 : 3;
}
