#pragma once
// Conservative import of prior installer records. Never delete an official class
// or UserChoice; legacy classes are retained with an official open command.
namespace ProductLegacy {
using namespace MariAssociationProxy;
inline bool exactLauncher(const Value& value, const std::wstring& launcher) {
    std::wstring command;
    return text(value, command) && command == L"\"" + launcher + L"\" \"%1\"";
}
inline bool isLegacyHandler(const std::wstring& name) {
    for (const auto* legacy : kLegacyHandlers) if (_wcsicmp(legacy, name.c_str()) == 0) return true;
    return false;
}
inline bool importOriginal(HKEY, const std::wstring& handler, const std::wstring& launcher,
                           const std::wstring& official, Value& original, std::wstring& error) {
    if (!exactLauncher(original, launcher)) return true;
    if (isLegacyHandler(handler)) {
        // Keep this legacy ProgID usable if Windows still references it.
        original = stringValue(L"\"" + official + L"\" \"%1\"");
        return true;
    }
    error = L"检测到旧版接管命令，但无法验证其原始备份。请保留备份并检查后重试。";
    return false;
}

inline bool restoreExtensions(HKEY user, const std::wstring& root, std::wstring& error, bool validateOnly = false) {
    const auto launcher = root + L"\\ChineseLauncher\\" + kLauncher;
    const auto official = root + L"\\" + hostName(root);
    for (size_t i = 0; i < kExtensions.size(); ++i) {
        if (i >= kLegacyHandlers.size()) break;
        const auto extPath = L"Software\\Classes\\" + std::wstring(kExtensions[i]);
        const auto classPath = L"Software\\Classes\\" + std::wstring(kLegacyHandlers[i]) + L"\\shell\\open\\command";
        Value current, command;
        std::wstring id, commandText;
        if (!read(user, extPath, nullptr, current) || !read(user, classPath, nullptr, command)) return false;
        if (!text(current, id) || id != kLegacyHandlers[i]) continue;
        if (!text(command, commandText) || (!exactLauncher(command, launcher) &&
            commandText != L"\"" + official + L"\" \"%1\"")) continue;
        const std::wstring backup = L"Software\\MariChineseLocalizer\\AssocBackup";
        const auto prefix = std::wstring(kExtensions[i]).substr(1);
        DWORD had = 0;
        if (!dword(user, backup, (prefix + L"_had_default").c_str(), had) || had > 1) {
            error = L"旧版文件关联备份不完整，已停止卸载。请保留安装目录与备份。";
            return false;
        }
        DWORD saved = 0;
        if (!dword(user, backup, (prefix + L"_saved").c_str(), saved) || saved != 1) return false;
        Value original;
        std::wstring originalId;
        if (had && (!read(user, backup, (prefix + L"_default").c_str(), original) ||
            !text(original, originalId) || originalId.empty() || originalId == id)) return false;
        if (validateOnly) continue;
        if (!write(user, extPath, nullptr, original)) return false;
        // Keep the old backup and ProgID: UserChoice may still refer to the latter.
        if (exactLauncher(command, launcher) && !write(user, classPath, nullptr,
            stringValue(L"\"" + official + L"\" \"%1\""))) return false;
    }
    return true;
}
}
