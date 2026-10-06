#include "../launcher.cpp"

#include <iostream>

int wmain(int argc, wchar_t** argv) {
    if (argc == 3 && wcscmp(argv[1], L"--child") == 0) {
        Sleep(static_cast<DWORD>(_wtoi(argv[2])));
        return 37;
    }

    const std::wstring executable = ExePath();
    if (!WaitForExistingMariTransition(executable, executable, 0) ||
        WaitForMariQt(GetCurrentProcess(), GetCurrentProcessId(), 0) !=
            QtReadiness::TimedOut) return 1;

    std::wstring command = L"\"" + executable + L"\" --child 2000";
    STARTUPINFOW startup{};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION child{};
    if (!CreateProcessW(executable.c_str(), command.data(), nullptr, nullptr,
                        FALSE, CREATE_NO_WINDOW, nullptr, nullptr,
                        &startup, &child)) return 2;
    Sleep(250);
    const bool timedOut = !WaitForExistingMariTransition(executable, executable, 200);
    const bool waited = WaitForExistingMariTransition(executable, executable, 5000);
    const bool exited = WaitForMariQt(child.hProcess, child.dwProcessId, 100) ==
                        QtReadiness::ProcessExited;
    DWORD exitCode = 0;
    const bool codeMatches = GetExitCodeProcess(child.hProcess, &exitCode) && exitCode == 37;
    CloseHandle(child.hThread);
    CloseHandle(child.hProcess);
    if (!timedOut || !waited || !exited || !codeMatches) return 3;
    std::wcout << L"Mari transition wait, timeout, and early exit=PASS\n";
    return 0;
}
