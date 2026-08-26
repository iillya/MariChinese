// ============================================================================
//  Mari 中文汉化 - 启动器
// ============================================================================
//  Mari 没有插件入口，所以这个启动器（与 Toolbag / SpeedTree 汉化器一致）
//  以 SUSPENDED 状态启动 Mari7.5v2.exe，用远端 LoadLibraryW 线程注入
//  MariChineseHook.dll，然后恢复运行。原程序文件从不修改；命令行参数
//  （例如 .mri 项目路径）原样透传给 Mari。
// ============================================================================

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>
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

// 找到 Mari 安装目录：向上找含 Mari7.5v2.exe 的目录；找不到则回退到
// Program Files\Mari7.5v2\Bundle\bin（Mari 出厂安装目录）。
std::wstring FindMariRoot(const std::wstring &start) {
    std::wstring dir = start;
    for (int depth = 0; depth < 12; ++depth) {
        if (IsFile(dir + L"\\Mari7.5v2.exe")) return dir;
        std::wstring parent = ParentDir(dir);
        if (parent.empty() || parent == dir) break;
        dir = parent;
    }
    wchar_t pf[MAX_PATH] = {};
    DWORD pfLen = GetEnvironmentVariableW(L"ProgramFiles", pf, MAX_PATH);
    if (pfLen == 0 || pfLen >= MAX_PATH)
        pfLen = GetEnvironmentVariableW(L"ProgramW6432", pf, MAX_PATH);
    if (pfLen && pfLen < MAX_PATH) {
        const std::wstring candidate = std::wstring(pf) + L"\\Mari7.5v2\\Bundle\\bin";
        if (IsFile(candidate + L"\\Mari7.5v2.exe")) return candidate;
    }
    return L"";
}

LPTHREAD_START_ROUTINE ResolveLoadLibrary(DWORD pid) {
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
    return reinterpret_cast<LPTHREAD_START_ROUTINE>(fn);
}

} // namespace

int APIENTRY wWinMain(HINSTANCE, HINSTANCE, PWSTR cmdLine, int) {
    const std::wstring own = ExePath();
    const std::wstring dir = ParentDir(own);
    const std::wstring root = FindMariRoot(dir);
    const std::wstring exePath = root + L"\\Mari7.5v2.exe";
    const std::wstring dllPath = dir + L"\\MariChineseHook.dll";

    if (root.empty() || !IsFile(dllPath) || !IsFile(exePath)) {
        MessageBoxW(nullptr,
                    L"找不到 Mari7.5v2.exe 或 汉化 DLL。\n"
                    L"请重新运行安装程序，修复 MariChineseLauncher 目录。",
                    L"Mari 中文补丁", MB_OK | MB_ICONERROR);
        return 1;
    }

    // 原始 Mari7.5v2_4K.bat 用 QT_SCALE_FACTOR 放大 UI；launcher 显式设置
    // 这三个环境变量，保证 Mari 一定能读到，从而让 4K DPI 适配（hook 里读
    // QT_SCALE_FACTOR 决定 3D/UV 视口 framebuffer 缩放）在注入后自动生效。
    SetEnvironmentVariableW(L"QT_ENABLE_HIGHDPI_SCALING", L"1");
    SetEnvironmentVariableW(L"QT_AUTO_SCREEN_SCALE_FACTOR", L"1");
    SetEnvironmentVariableW(L"QT_SCALE_FACTOR", L"2");

    STARTUPINFOW si{}; si.cb = sizeof(si);
    PROCESS_INFORMATION pi{};
    std::wstring cl = L"\"" + exePath + L"\"";
    if (cmdLine && *cmdLine) { cl += L" "; cl += cmdLine; }
    std::vector<wchar_t> clBuf(cl.begin(), cl.end()); clBuf.push_back(L'\0');

    if (!CreateProcessW(exePath.c_str(), clBuf.data(), nullptr, nullptr, FALSE,
                        CREATE_SUSPENDED, nullptr, root.c_str(), &si, &pi)) {
        MessageBoxW(nullptr, L"无法启动 Mari7.5v2.exe。",
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

    auto loadLib = ResolveLoadLibrary(pi.dwProcessId);
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
