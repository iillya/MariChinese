#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>

#include <cwchar>
#include <string>
#include <vector>

namespace {

bool isFile(const std::wstring &path) {
    const DWORD attributes = GetFileAttributesW(path.c_str());
    return attributes != INVALID_FILE_ATTRIBUTES &&
           !(attributes & FILE_ATTRIBUTE_DIRECTORY);
}

std::wstring findMariInDirectory(const std::wstring &directory) {
    WIN32_FIND_DATAW data{};
    HANDLE search = FindFirstFileW((directory + L"\\Mari*.exe").c_str(), &data);
    if (search == INVALID_HANDLE_VALUE) return {};
    std::wstring result;
    do {
        const std::wstring name = data.cFileName;
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
            name.size() > 4 && name[4] >= L'0' && name[4] <= L'9') {
            result = directory + L"\\" + name;
            break;
        }
    } while (FindNextFileW(search, &data));
    FindClose(search);
    return result;
}

std::wstring findMariExecutable() {
    wchar_t configured[32768]{};
    const DWORD configuredLength = GetEnvironmentVariableW(
        L"MARI_DPI_TEST_EXE", configured,
        static_cast<DWORD>(_countof(configured)));
    if (configuredLength && configuredLength < _countof(configured) &&
        isFile(configured))
        return configured;

    wchar_t programFiles[MAX_PATH]{};
    const DWORD length = GetEnvironmentVariableW(
        L"ProgramFiles", programFiles,
        static_cast<DWORD>(_countof(programFiles)));
    if (!length || length >= _countof(programFiles)) return {};
    WIN32_FIND_DATAW data{};
    HANDLE search = FindFirstFileW(
        (std::wstring(programFiles) + L"\\Mari*").c_str(), &data);
    if (search == INVALID_HANDLE_VALUE) return {};
    std::wstring result;
    do {
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) continue;
        const std::wstring candidate = std::wstring(programFiles) + L"\\" +
            data.cFileName + L"\\Bundle\\bin";
        const std::wstring found = findMariInDirectory(candidate);
        if (!found.empty() &&
            (result.empty() || _wcsicmp(found.c_str(), result.c_str()) > 0))
            result = found;
    } while (FindNextFileW(search, &data));
    FindClose(search);
    return result;
}

std::wstring parentDir(const std::wstring &path) {
    const size_t slash = path.find_last_of(L"\\/");
    return slash == std::wstring::npos ? L"" : path.substr(0, slash);
}

std::wstring ownPath() {
    std::vector<wchar_t> buffer(1024);
    while (buffer.size() <= 32768) {
        const DWORD size = GetModuleFileNameW(nullptr, buffer.data(),
                                             static_cast<DWORD>(buffer.size()));
        if (!size) return L"";
        if (size < buffer.size() - 1) return std::wstring(buffer.data(), size);
        buffer.resize(buffer.size() * 2);
    }
    return L"";
}

LPTHREAD_START_ROUTINE remoteLoadLibrary(DWORD pid) {
    HMODULE localKernel = GetModuleHandleW(L"kernel32.dll");
    FARPROC localLoadLibrary = localKernel
        ? GetProcAddress(localKernel, "LoadLibraryW") : nullptr;
    if (!localKernel || !localLoadLibrary) return nullptr;
    const uintptr_t offset = reinterpret_cast<uintptr_t>(localLoadLibrary) -
                             reinterpret_cast<uintptr_t>(localKernel);
    HANDLE snapshot = CreateToolhelp32Snapshot(
        TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
    if (snapshot == INVALID_HANDLE_VALUE) return nullptr;
    MODULEENTRY32W module{};
    module.dwSize = sizeof(module);
    LPTHREAD_START_ROUTINE result = nullptr;
    if (Module32FirstW(snapshot, &module)) {
        do {
            if (_wcsicmp(module.szModule, L"kernel32.dll") == 0) {
                result = reinterpret_cast<LPTHREAD_START_ROUTINE>(
                    reinterpret_cast<uintptr_t>(module.modBaseAddr) + offset);
                break;
            }
        } while (Module32NextW(snapshot, &module));
    }
    CloseHandle(snapshot);
    return result;
}

bool waitForModule(DWORD pid, const wchar_t *moduleName, DWORD timeoutMs) {
    const DWORD started = GetTickCount();
    while (GetTickCount() - started < timeoutMs) {
        HANDLE snapshot = CreateToolhelp32Snapshot(
            TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
        if (snapshot != INVALID_HANDLE_VALUE) {
            MODULEENTRY32W module{};
            module.dwSize = sizeof(module);
            if (Module32FirstW(snapshot, &module)) {
                do {
                    if (_wcsicmp(module.szModule, moduleName) == 0) {
                        CloseHandle(snapshot);
                        return true;
                    }
                } while (Module32NextW(snapshot, &module));
            }
            CloseHandle(snapshot);
        }
        Sleep(100);
    }
    return false;
}

} // namespace

int APIENTRY wWinMain(HINSTANCE, HINSTANCE, PWSTR commandLine, int) {
    const std::wstring directory = parentDir(ownPath());
    const std::wstring dllPath = directory + L"\\MariDpiVtableTest.dll";
    const std::wstring exePath = findMariExecutable();
    if (!isFile(exePath) || !isFile(dllPath)) {
        MessageBoxW(nullptr, L"找不到 Mari 主程序或 DPI 实验 DLL。",
                    L"Mari DPI 实验", MB_OK | MB_ICONERROR);
        return 1;
    }

    // Use Mari's native Qt scaling environment before process creation.
    // MARI_DPI_TEST_SCALE allows controlled A/B tests; normal runs remain 2.0.
    wchar_t scale[32] = L"2";
    const DWORD scaleLength = GetEnvironmentVariableW(
        L"MARI_DPI_TEST_SCALE", scale, static_cast<DWORD>(_countof(scale)));
    if (!scaleLength || scaleLength >= _countof(scale))
        wcscpy_s(scale, L"2");
    SetEnvironmentVariableW(L"QT_ENABLE_HIGHDPI_SCALING", L"1");
    SetEnvironmentVariableW(L"QT_AUTO_SCREEN_SCALE_FACTOR", L"1");
    SetEnvironmentVariableW(L"QT_SCALE_FACTOR", scale);

    std::wstring fullCommand = L"\"" + exePath + L"\"";
    if (commandLine && *commandLine) fullCommand += L" " + std::wstring(commandLine);
    std::vector<wchar_t> command(fullCommand.begin(), fullCommand.end());
    command.push_back(L'\0');
    STARTUPINFOW startup{};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION process{};
    const std::wstring workDir = parentDir(exePath);
    if (!CreateProcessW(exePath.c_str(), command.data(), nullptr, nullptr, FALSE,
                        0, nullptr, workDir.c_str(), &startup, &process)) {
        MessageBoxW(nullptr, L"无法启动 Mari。", L"Mari DPI 实验",
                    MB_OK | MB_ICONERROR);
        return 2;
    }

    // Native Qt scaling is already active from process creation. This DPI-only
    // experiment can wait until Qt is initialized instead of injecting into a
    // process whose Qt dependencies have not been loaded yet.
    if (!waitForModule(process.dwProcessId, L"Qt5Widgets.dll", 30000)) {
        TerminateProcess(process.hProcess, 3);
        CloseHandle(process.hThread);
        CloseHandle(process.hProcess);
        MessageBoxW(nullptr, L"等待 Qt5Widgets.dll 超时。", L"Mari DPI 实验",
                    MB_OK | MB_ICONERROR);
        return 3;
    }

    const SIZE_T bytes = (dllPath.size() + 1) * sizeof(wchar_t);
    void *remote = VirtualAllocEx(process.hProcess, nullptr, bytes,
        MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    SIZE_T written = 0;
    HANDLE thread = nullptr;
    if (remote && WriteProcessMemory(process.hProcess, remote, dllPath.c_str(),
                                     bytes, &written) && written == bytes) {
        if (auto loadLibrary = remoteLoadLibrary(process.dwProcessId))
            thread = CreateRemoteThread(process.hProcess, nullptr, 0,
                                        loadLibrary, remote, 0, nullptr);
    }
    bool loaded = false;
    bool remoteThreadCompleted = false;
    if (thread) {
        const DWORD wait = WaitForSingleObject(thread, 30000);
        remoteThreadCompleted = wait == WAIT_OBJECT_0;
        DWORD result = 0;
        loaded = wait == WAIT_OBJECT_0 && GetExitCodeThread(thread, &result) && result;
        CloseHandle(thread);
    }
    if (!loaded) {
        TerminateProcess(process.hProcess, 3);
        WaitForSingleObject(process.hProcess, 5000);
        MessageBoxW(nullptr, L"DPI 实验注入失败。", L"Mari DPI 实验",
                    MB_OK | MB_ICONERROR);
    }
    if (remote && (remoteThreadCompleted || !loaded))
        VirtualFreeEx(process.hProcess, remote, 0, MEM_RELEASE);
    CloseHandle(process.hThread);
    CloseHandle(process.hProcess);
    return loaded ? 0 : 4;
}
