#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <bcrypt.h>
#include <commctrl.h>
#include <dwmapi.h>
#include <shlobj.h>
#include <shobjidl.h>

#include <cstdint>
#include <cstring>
#include <cwchar>
#include <cwctype>
#include <filesystem>
#include <fstream>
#include <limits>
#include <string>
#include <vector>

#pragma comment(lib, "Comctl32.lib")
#pragma comment(lib, "bcrypt.lib")
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(linker, "/manifestdependency:\"type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

namespace {

constexpr uint64_t kMagic = 0x314952414D4843ull;
constexpr int kDirectoryEdit = 1001;
constexpr int kBrowseButton = 1002;
constexpr int kDpiCheck = 1003;
constexpr int kScaleEdit = 1004;
constexpr int kInstallButton = 1005;
constexpr int kUninstallButton = 1006;
constexpr int kTitleLabel = 1010;
constexpr int kSubtitleLabel = 1011;
constexpr int kPathLabel = 1012;
constexpr int kDpiHintLabel = 1013;
constexpr int kScaleLabel = 1014;
const wchar_t *kTitle = L"Mari 中文补丁安装程序";

struct PayloadEntry {
    std::wstring name;
    uint64_t offset = 0;
    uint64_t size = 0;
    BYTE digest[32]{};
};

struct State {
    std::wstring directory;
    std::vector<BYTE> executable;
    std::vector<PayloadEntry> entries;
    HWND directoryEdit = nullptr;
    HWND dpiCheck = nullptr;
    HWND scaleEdit = nullptr;
    HFONT font = nullptr;
    HFONT titleFont = nullptr;
    HFONT semiboldFont = nullptr;
    HBRUSH backgroundBrush = nullptr;
    HBRUSH cardBrush = nullptr;
    HBRUSH editBrush = nullptr;
    HICON windowIcon = nullptr;
    int operation = 0;
    bool dpiEnabled = true;
    std::wstring scale = L"1.75";
};

int DpiValue(int value, UINT dpi) { return MulDiv(value, static_cast<int>(dpi), 96); }

bool IsFile(const std::wstring &path) {
    const DWORD attributes = GetFileAttributesW(path.c_str());
    return attributes != INVALID_FILE_ATTRIBUTES &&
           !(attributes & FILE_ATTRIBUTE_DIRECTORY);
}

std::wstring OwnPath() {
    std::vector<wchar_t> buffer(1024);
    while (buffer.size() <= 32768) {
        const DWORD length = GetModuleFileNameW(
            nullptr, buffer.data(), static_cast<DWORD>(buffer.size()));
        if (!length) return {};
        if (length < buffer.size() - 1)
            return std::wstring(buffer.data(), length);
        buffer.resize(buffer.size() * 2);
    }
    return {};
}

bool HasMariExecutable(const std::wstring &directory) {
    WIN32_FIND_DATAW data{};
    HANDLE search = FindFirstFileW((directory + L"\\Mari*.exe").c_str(), &data);
    if (search == INVALID_HANDLE_VALUE) return false;
    bool found = false;
    do {
        const std::wstring name = data.cFileName;
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
            name.size() > 4 && iswdigit(name[4])) {
            found = true;
            break;
        }
    } while (FindNextFileW(search, &data));
    FindClose(search);
    return found;
}

std::wstring FindDefaultDirectory() {
    wchar_t programFiles[MAX_PATH]{};
    const DWORD length = GetEnvironmentVariableW(
        L"ProgramFiles", programFiles, static_cast<DWORD>(_countof(programFiles)));
    if (!length || length >= _countof(programFiles)) return {};
    WIN32_FIND_DATAW data{};
    HANDLE search = FindFirstFileW((std::wstring(programFiles) + L"\\Mari*").c_str(),
                                   &data);
    if (search == INVALID_HANDLE_VALUE) return {};
    std::wstring result;
    do {
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) ||
            wcscmp(data.cFileName, L".") == 0 || wcscmp(data.cFileName, L"..") == 0)
            continue;
        const std::wstring candidate = std::wstring(programFiles) + L"\\" +
                                       data.cFileName + L"\\Bundle\\bin";
        if (HasMariExecutable(candidate) &&
            (result.empty() || _wcsicmp(candidate.c_str(), result.c_str()) > 0))
            result = candidate;
    } while (FindNextFileW(search, &data));
    FindClose(search);
    return result;
}

bool Utf8ToWide(const std::string &source, std::wstring &destination) {
    if (source.empty()) return false;
    const int count = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS,
                                          source.data(), static_cast<int>(source.size()),
                                          nullptr, 0);
    if (count <= 0) return false;
    destination.resize(count);
    return MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, source.data(),
                               static_cast<int>(source.size()), destination.data(),
                               count) == count;
}

bool SafePayloadName(const std::wstring &name) {
    if (name.empty() || name.find(L':') != std::wstring::npos) return false;
    const std::filesystem::path path(name);
    if (path.is_absolute() || path.has_root_path()) return false;
    for (const auto &part : path) {
        if (part.empty() || part == L"." || part == L"..") return false;
    }
    return true;
}

template <typename T>
bool ReadValue(const std::vector<BYTE> &data, size_t &position, T &value) {
    if (position > data.size() || sizeof(T) > data.size() - position) return false;
    memcpy(&value, data.data() + position, sizeof(T));
    position += sizeof(T);
    return true;
}

bool LoadPayload(State &state) {
    std::ifstream stream(OwnPath(), std::ios::binary);
    if (!stream) return false;
    stream.seekg(0, std::ios::end);
    const auto length = stream.tellg();
    if (length <= 0) return false;
    state.executable.resize(static_cast<size_t>(length));
    stream.seekg(0);
    stream.read(reinterpret_cast<char *>(state.executable.data()), length);
    if (!stream) return false;

    constexpr size_t tailSize = sizeof(uint32_t) * 2 + sizeof(uint64_t);
    if (state.executable.size() < tailSize) return false;
    size_t tail = state.executable.size() - tailSize;
    uint32_t manifestSize = 0, count = 0;
    uint64_t magic = 0;
    if (!ReadValue(state.executable, tail, manifestSize) ||
        !ReadValue(state.executable, tail, count) ||
        !ReadValue(state.executable, tail, magic) || magic != kMagic ||
        manifestSize > state.executable.size() - tailSize) return false;
    size_t position = state.executable.size() - tailSize - manifestSize;
    const size_t payloadEnd = position;
    const size_t manifestEnd = state.executable.size() - tailSize;
    if (count == 0 || count > 64) return false;
    for (uint32_t index = 0; index < count; ++index) {
        uint32_t nameLength = 0;
        if (position > manifestEnd ||
            !ReadValue(state.executable, position, nameLength) ||
            position > manifestEnd ||
            nameLength > manifestEnd - position) return false;
        const std::string utf8(reinterpret_cast<const char *>(
            state.executable.data() + position), nameLength);
        position += nameLength;
        PayloadEntry entry;
        if (!Utf8ToWide(utf8, entry.name) || !SafePayloadName(entry.name) ||
            !ReadValue(state.executable, position, entry.offset) ||
            !ReadValue(state.executable, position, entry.size) ||
            position + sizeof(entry.digest) > manifestEnd ||
            entry.offset > payloadEnd || entry.size > payloadEnd - entry.offset)
            return false;
        memcpy(entry.digest, state.executable.data() + position,
               sizeof(entry.digest));
        position += sizeof(entry.digest);
        state.entries.push_back(entry);
    }
    return position == manifestEnd && !state.entries.empty();
}

bool HashMatches(const State &state, const PayloadEntry &entry) {
    if (entry.size > (std::numeric_limits<ULONG>::max)()) return false;
    BCRYPT_ALG_HANDLE algorithm = nullptr;
    BCRYPT_HASH_HANDLE hash = nullptr;
    DWORD objectSize = 0, hashSize = 0, returned = 0;
    bool ok = BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_SHA256_ALGORITHM,
                                          nullptr, 0) == 0 &&
              BCryptGetProperty(algorithm, BCRYPT_OBJECT_LENGTH,
                reinterpret_cast<BYTE *>(&objectSize), sizeof(objectSize),
                &returned, 0) == 0 &&
              BCryptGetProperty(algorithm, BCRYPT_HASH_LENGTH,
                reinterpret_cast<BYTE *>(&hashSize), sizeof(hashSize),
                &returned, 0) == 0 && hashSize == sizeof(entry.digest);
    std::vector<BYTE> object(ok ? objectSize : 0);
    BYTE digest[32]{};
    if (ok) ok = BCryptCreateHash(algorithm, &hash, object.data(), objectSize,
                                  nullptr, 0, 0) == 0 &&
                 BCryptHashData(hash, const_cast<BYTE *>(state.executable.data() +
                    entry.offset), static_cast<ULONG>(entry.size), 0) == 0 &&
                 BCryptFinishHash(hash, digest, sizeof(digest), 0) == 0 &&
                 memcmp(digest, entry.digest, sizeof(digest)) == 0;
    if (hash) BCryptDestroyHash(hash);
    if (algorithm) BCryptCloseAlgorithmProvider(algorithm, 0);
    return ok;
}

std::wstring ControlText(HWND control) {
    const int length = GetWindowTextLengthW(control);
    std::wstring text(static_cast<size_t>(length) + 1, L'\0');
    GetWindowTextW(control, text.data(), length + 1);
    text.resize(length);
    return text;
}

bool CreateShortcut(const std::wstring &path, const std::wstring &target,
                    const std::wstring &workingDirectory) {
    IShellLinkW *link = nullptr;
    if (FAILED(CoCreateInstance(CLSID_ShellLink, nullptr, CLSCTX_INPROC_SERVER,
                                IID_PPV_ARGS(&link)))) return false;
    link->SetPath(target.c_str());
    link->SetWorkingDirectory(workingDirectory.c_str());
    link->SetDescription(L"通过 Mari 中文补丁启动");
    IPersistFile *file = nullptr;
    const bool ok = SUCCEEDED(link->QueryInterface(IID_PPV_ARGS(&file))) &&
                    SUCCEEDED(file->Save(path.c_str(), TRUE));
    if (file) file->Release();
    link->Release();
    return ok;
}

std::wstring KnownFolder(REFKNOWNFOLDERID id) {
    PWSTR value = nullptr;
    std::wstring result;
    if (SUCCEEDED(SHGetKnownFolderPath(id, 0, nullptr, &value)) && value)
        result = value;
    CoTaskMemFree(value);
    return result;
}

bool WriteSettings(const std::filesystem::path &installDirectory,
                   bool dpiEnabled, const std::wstring &scale) {
    const std::wstring path = (installDirectory / L"settings.ini").wstring();
    return WritePrivateProfileStringW(L"Dpi", L"Enabled",
               dpiEnabled ? L"1" : L"0", path.c_str()) &&
           WritePrivateProfileStringW(L"Dpi", L"ScaleFactor", scale.c_str(),
                                      path.c_str());
}

struct MariAssociation {
    const wchar_t *extension;
    const wchar_t *progId;
    const wchar_t *description;
    const wchar_t *backupPrefix;
};

constexpr MariAssociation kMariAssociations[] = {
    {L".mra", L"MariChinese.mra", L"Mari 项目归档", L"mra"},
    {L".mnc", L"MariChinese.mnc", L"Mari 非商业项目归档", L"mnc"},
    {L".mri", L"MariChinese.mri", L"Mari 项目文件", L"mri"},
};

std::wstring FindMariExecutable(const std::wstring &directory) {
    WIN32_FIND_DATAW data{};
    HANDLE search = FindFirstFileW((directory + L"\\Mari*.exe").c_str(), &data);
    if (search == INVALID_HANDLE_VALUE) return {};
    std::wstring result;
    do {
        const std::wstring name = data.cFileName;
        if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) &&
            name.size() > 4 && iswdigit(name[4])) {
            result = directory + L"\\" + name;
            break;
        }
    } while (FindNextFileW(search, &data));
    FindClose(search);
    return result;
}

bool ReadRegistryString(HKEY root, const std::wstring &path,
                        const wchar_t *name, std::wstring &value) {
    HKEY key = nullptr;
    if (RegOpenKeyExW(root, path.c_str(), 0, KEY_QUERY_VALUE, &key) != ERROR_SUCCESS)
        return false;
    DWORD type = 0, bytes = 0;
    LONG status = RegQueryValueExW(key, name, nullptr, &type, nullptr, &bytes);
    if (status != ERROR_SUCCESS || (type != REG_SZ && type != REG_EXPAND_SZ) ||
        bytes < sizeof(wchar_t)) {
        RegCloseKey(key);
        return false;
    }
    std::vector<wchar_t> buffer(bytes / sizeof(wchar_t) + 1, L'\0');
    status = RegQueryValueExW(key, name, nullptr, &type,
                              reinterpret_cast<BYTE *>(buffer.data()), &bytes);
    RegCloseKey(key);
    if (status != ERROR_SUCCESS) return false;
    value.assign(buffer.data());
    return true;
}

bool WriteRegistryString(HKEY root, const std::wstring &path,
                         const wchar_t *name, const std::wstring &value) {
    HKEY key = nullptr;
    if (RegCreateKeyExW(root, path.c_str(), 0, nullptr, 0,
                        KEY_SET_VALUE, nullptr, &key, nullptr) != ERROR_SUCCESS)
        return false;
    const LONG status = RegSetValueExW(
        key, name, 0, REG_SZ, reinterpret_cast<const BYTE *>(value.c_str()),
        static_cast<DWORD>((value.size() + 1) * sizeof(wchar_t)));
    RegCloseKey(key);
    return status == ERROR_SUCCESS;
}

bool BackupAssociation(const MariAssociation &association) {
    const std::wstring backupPath =
        L"Software\\MariChineseLocalizer\\AssocBackup";
    const std::wstring savedName =
        std::wstring(association.backupPrefix) + L"_saved";
    HKEY key = nullptr;
    if (RegCreateKeyExW(HKEY_CURRENT_USER, backupPath.c_str(), 0, nullptr, 0,
                        KEY_READ | KEY_WRITE, nullptr, &key, nullptr) != ERROR_SUCCESS)
        return false;
    DWORD saved = 0, bytes = sizeof(saved);
    if (RegQueryValueExW(key, savedName.c_str(), nullptr, nullptr,
                         reinterpret_cast<BYTE *>(&saved), &bytes) == ERROR_SUCCESS &&
        saved != 0) {
        RegCloseKey(key);
        return true;
    }

    const std::wstring extensionPath =
        std::wstring(L"Software\\Classes\\") + association.extension;
    std::wstring current;
    const bool hadDefault = ReadRegistryString(
        HKEY_CURRENT_USER, extensionPath, nullptr, current) &&
        _wcsicmp(current.c_str(), association.progId) != 0;
    const std::wstring hadName =
        std::wstring(association.backupPrefix) + L"_had_default";
    const std::wstring defaultName =
        std::wstring(association.backupPrefix) + L"_default";
    DWORD had = hadDefault ? 1u : 0u;
    bool ok = RegSetValueExW(key, hadName.c_str(), 0, REG_DWORD,
                    reinterpret_cast<const BYTE *>(&had), sizeof(had)) == ERROR_SUCCESS;
    if (ok && hadDefault) {
        ok = RegSetValueExW(key, defaultName.c_str(), 0, REG_SZ,
                 reinterpret_cast<const BYTE *>(current.c_str()),
                 static_cast<DWORD>((current.size() + 1) * sizeof(wchar_t))) == ERROR_SUCCESS;
    }
    if (ok) {
        saved = 1;
        ok = RegSetValueExW(key, savedName.c_str(), 0, REG_DWORD,
                    reinterpret_cast<const BYTE *>(&saved), sizeof(saved)) == ERROR_SUCCESS;
    }
    RegCloseKey(key);
    return ok;
}

bool RegisterMariAssociations(const std::wstring &launcher,
                              const std::wstring &mariExecutable) {
    bool ok = true;
    for (const MariAssociation &association : kMariAssociations) {
        ok = BackupAssociation(association) && ok;
        const std::wstring extensionPath =
            std::wstring(L"Software\\Classes\\") + association.extension;
        const std::wstring progIdPath =
            std::wstring(L"Software\\Classes\\") + association.progId;
        ok = WriteRegistryString(HKEY_CURRENT_USER, extensionPath, nullptr,
                                 association.progId) && ok;
        ok = WriteRegistryString(HKEY_CURRENT_USER, progIdPath, nullptr,
                                 association.description) && ok;
        ok = WriteRegistryString(HKEY_CURRENT_USER,
                 progIdPath + L"\\DefaultIcon", nullptr,
                 L"\"" + mariExecutable + L"\",0") && ok;
        ok = WriteRegistryString(HKEY_CURRENT_USER,
                 progIdPath + L"\\shell\\open\\command", nullptr,
                 L"\"" + launcher + L"\" \"%1\"") && ok;

        HKEY openWith = nullptr;
        if (RegCreateKeyExW(HKEY_CURRENT_USER,
                (extensionPath + L"\\OpenWithProgids").c_str(), 0, nullptr, 0,
                KEY_SET_VALUE, nullptr, &openWith, nullptr) == ERROR_SUCCESS) {
            const BYTE empty = 0;
            ok = RegSetValueExW(openWith, association.progId, 0, REG_NONE,
                                &empty, 0) == ERROR_SUCCESS && ok;
            RegCloseKey(openWith);
        } else {
            ok = false;
        }
    }
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, nullptr, nullptr);
    return ok;
}

void RestoreMariAssociations() {
    const std::wstring backupPath =
        L"Software\\MariChineseLocalizer\\AssocBackup";
    HKEY backup = nullptr;
    RegOpenKeyExW(HKEY_CURRENT_USER, backupPath.c_str(), 0, KEY_QUERY_VALUE,
                  &backup);
    for (const MariAssociation &association : kMariAssociations) {
        const std::wstring extensionPath =
            std::wstring(L"Software\\Classes\\") + association.extension;
        std::wstring current;
        if (ReadRegistryString(HKEY_CURRENT_USER, extensionPath, nullptr, current) &&
            _wcsicmp(current.c_str(), association.progId) == 0) {
            DWORD hadDefault = 0, bytes = sizeof(hadDefault);
            const std::wstring hadName =
                std::wstring(association.backupPrefix) + L"_had_default";
            if (backup && RegQueryValueExW(backup, hadName.c_str(), nullptr,
                    nullptr, reinterpret_cast<BYTE *>(&hadDefault), &bytes) == ERROR_SUCCESS &&
                hadDefault != 0) {
                const std::wstring defaultName =
                    std::wstring(association.backupPrefix) + L"_default";
                std::wstring value;
                if (ReadRegistryString(HKEY_CURRENT_USER, backupPath,
                                       defaultName.c_str(), value))
                    WriteRegistryString(HKEY_CURRENT_USER, extensionPath,
                                        nullptr, value);
            } else {
                HKEY extension = nullptr;
                if (RegOpenKeyExW(HKEY_CURRENT_USER, extensionPath.c_str(), 0,
                                  KEY_SET_VALUE, &extension) == ERROR_SUCCESS) {
                    RegDeleteValueW(extension, nullptr);
                    RegCloseKey(extension);
                }
            }
        }
        RegDeleteTreeW(HKEY_CURRENT_USER,
            (std::wstring(L"Software\\Classes\\") + association.progId).c_str());
        HKEY openWith = nullptr;
        if (RegOpenKeyExW(HKEY_CURRENT_USER,
                (extensionPath + L"\\OpenWithProgids").c_str(), 0,
                KEY_SET_VALUE, &openWith) == ERROR_SUCCESS) {
            RegDeleteValueW(openWith, association.progId);
            RegCloseKey(openWith);
        }
    }
    if (backup) RegCloseKey(backup);
    RegDeleteTreeW(HKEY_CURRENT_USER, backupPath.c_str());
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, nullptr, nullptr);
}

bool Install(const State &state, bool dpiEnabled, const std::wstring &scale) {
    const std::filesystem::path install =
        std::filesystem::path(state.directory) / L"ChineseLauncher";
    const std::filesystem::path staging =
        std::filesystem::path(state.directory) / L"ChineseLauncher.new";
    const std::filesystem::path backup =
        std::filesystem::path(state.directory) / L"ChineseLauncher.old";
    std::error_code error;
    const auto discardStaging = [&] {
        std::error_code ignored;
        std::filesystem::remove_all(staging, ignored);
    };
    std::filesystem::remove_all(staging, error);
    if (error) return false;
    std::filesystem::create_directories(staging, error);
    if (error) return false;
    for (const PayloadEntry &entry : state.entries) {
        if (!HashMatches(state, entry)) {
            discardStaging();
            return false;
        }
        const std::filesystem::path destination = staging / entry.name;
        std::filesystem::create_directories(destination.parent_path(), error);
        if (error) {
            discardStaging();
            return false;
        }
        std::ofstream output(destination, std::ios::binary | std::ios::trunc);
        output.write(reinterpret_cast<const char *>(state.executable.data() +
                     entry.offset), static_cast<std::streamsize>(entry.size));
        if (!output) {
            discardStaging();
            return false;
        }
    }
    if (!WriteSettings(staging, dpiEnabled, scale)) {
        discardStaging();
        return false;
    }
    std::filesystem::remove_all(backup, error);
    if (error) return false;
    const bool replacingExistingInstall = std::filesystem::exists(install);
    if (replacingExistingInstall) {
        std::filesystem::rename(install, backup, error);
        if (error) {
            discardStaging();
            return false;
        }
    }
    std::filesystem::rename(staging, install, error);
    if (error) {
        std::error_code restoreError;
        if (std::filesystem::exists(backup))
            std::filesystem::rename(backup, install, restoreError);
        return false;
    }
    const std::wstring launcher = (install / L"MariChineseLauncher.exe").wstring();
    const std::wstring shortcutName = L"Mari 中文版.lnk";
    const std::wstring desktop = KnownFolder(FOLDERID_PublicDesktop);
    const std::wstring programs = KnownFolder(FOLDERID_CommonPrograms);
    const std::wstring desktopShortcut = desktop.empty()
        ? L"" : desktop + L"\\" + shortcutName;
    const std::wstring programsShortcut = programs.empty()
        ? L"" : programs + L"\\" + shortcutName;
    bool shortcutsOk = true;
    if (!desktopShortcut.empty())
        shortcutsOk = CreateShortcut(desktopShortcut, launcher,
                                     state.directory) && shortcutsOk;
    if (!programsShortcut.empty())
        shortcutsOk = CreateShortcut(programsShortcut, launcher,
                                     state.directory) && shortcutsOk;
    const std::wstring mariExecutable = FindMariExecutable(state.directory);
    const bool associationsOk = !mariExecutable.empty() &&
        RegisterMariAssociations(launcher, mariExecutable);
    if (!shortcutsOk || !associationsOk) {
        if (!desktopShortcut.empty()) DeleteFileW(desktopShortcut.c_str());
        if (!programsShortcut.empty()) DeleteFileW(programsShortcut.c_str());
        std::error_code ignored;
        std::filesystem::remove_all(install, ignored);
        if (std::filesystem::exists(backup))
            std::filesystem::rename(backup, install, ignored);
        if (replacingExistingInstall && std::filesystem::exists(install)) {
            // 重装失败时恢复旧版文件和它的入口，不要把原始
            // 关联备份当成本次临时状态删掉。
            if (!desktopShortcut.empty())
                CreateShortcut(desktopShortcut, launcher, state.directory);
            if (!programsShortcut.empty())
                CreateShortcut(programsShortcut, launcher, state.directory);
            if (!mariExecutable.empty())
                RegisterMariAssociations(launcher, mariExecutable);
        } else {
            RestoreMariAssociations();
        }
        return false;
    }
    // 旧版备份只在所有安装步骤成功后删除；清理失败不应
    // 把一次已经成功的安装报成失败。
    std::filesystem::remove_all(backup, error);
    return true;
}

bool Uninstall(const State &state) {
    RestoreMariAssociations();
    std::error_code error;
    std::filesystem::remove_all(
        std::filesystem::path(state.directory) / L"ChineseLauncher", error);
    const std::wstring shortcutName = L"Mari 中文版.lnk";
    for (REFKNOWNFOLDERID id : {FOLDERID_PublicDesktop,
                                FOLDERID_CommonPrograms}) {
        const std::wstring folder = KnownFolder(id);
        if (!folder.empty()) DeleteFileW((folder + L"\\" + shortcutName).c_str());
    }
    return !error;
}

bool ChooseDirectory(std::wstring &directory) {
    BROWSEINFOW info{};
    info.lpszTitle = L"请选择包含 Mari 可执行文件的 Bundle\\bin 目录";
    info.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE;
    PIDLIST_ABSOLUTE item = SHBrowseForFolderW(&info);
    if (!item) return false;
    wchar_t path[MAX_PATH]{};
    const bool ok = SHGetPathFromIDListW(item, path) != FALSE;
    CoTaskMemFree(item);
    if (ok) directory = path;
    return ok;
}

bool ValidScale(const std::wstring &text) {
    wchar_t *end = nullptr;
    const double value = wcstod(text.c_str(), &end);
    return end != text.c_str() && *end == L'\0' && value >= 1.0 && value <= 3.0;
}

HFONT CreateUiFont(UINT dpi, int points, int weight) {
    return CreateFontW(-MulDiv(points, static_cast<int>(dpi), 72), 0, 0, 0,
        weight, FALSE, FALSE, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS,
        CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH,
        L"Segoe UI");
}

void FillRoundedRect(HDC dc, const RECT &rect, int radius, COLORREF color) {
    HBRUSH brush = CreateSolidBrush(color);
    HPEN pen = CreatePen(PS_SOLID, 1, color);
    HGDIOBJ oldBrush = SelectObject(dc, brush);
    HGDIOBJ oldPen = SelectObject(dc, pen);
    RoundRect(dc, rect.left, rect.top, rect.right, rect.bottom, radius, radius);
    SelectObject(dc, oldPen);
    SelectObject(dc, oldBrush);
    DeleteObject(pen);
    DeleteObject(brush);
}

void DrawRoundedOutline(HDC dc, const RECT &rect, int radius,
                        COLORREF color, int width = 1) {
    HPEN pen = CreatePen(PS_SOLID, width, color);
    HGDIOBJ oldPen = SelectObject(dc, pen);
    HGDIOBJ oldBrush = SelectObject(dc, GetStockObject(NULL_BRUSH));
    RoundRect(dc, rect.left, rect.top, rect.right, rect.bottom, radius, radius);
    SelectObject(dc, oldBrush);
    SelectObject(dc, oldPen);
    DeleteObject(pen);
}

void DrawModernButton(const DRAWITEMSTRUCT *item, const State &state) {
    const bool primary = item->CtlID == kInstallButton;
    const bool pressed = (item->itemState & ODS_SELECTED) != 0;
    const bool disabled = (item->itemState & ODS_DISABLED) != 0;
    COLORREF background = primary ? RGB(0, 103, 192) : RGB(231, 234, 238);
    COLORREF foreground = primary ? RGB(255, 255, 255) : RGB(38, 42, 48);
    if (pressed)
        background = primary ? RGB(0, 78, 152) : RGB(218, 221, 226);
    if (disabled) {
        background = RGB(232, 234, 237);
        foreground = RGB(145, 149, 156);
    }
    RECT rect = item->rcItem;
    const UINT dpi = GetDpiForWindow(item->hwndItem);
    const int radius = DpiValue(8, dpi);
    FillRoundedRect(item->hDC, rect, radius, background);
    DrawRoundedOutline(item->hDC, rect, radius,
        primary ? RGB(0, 83, 158) : RGB(176, 181, 188),
        DpiValue(1, dpi));
    wchar_t text[128]{};
    GetWindowTextW(item->hwndItem, text, static_cast<int>(_countof(text)));
    SetBkMode(item->hDC, TRANSPARENT);
    SetTextColor(item->hDC, foreground);
    HGDIOBJ oldFont = SelectObject(item->hDC, state.semiboldFont);
    DrawTextW(item->hDC, text, -1, &rect,
              DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    SelectObject(item->hDC, oldFont);
    if (item->itemState & ODS_FOCUS) {
        InflateRect(&rect, -DpiValue(3, dpi), -DpiValue(3, dpi));
        HPEN focus = CreatePen(PS_DOT, 1, primary ? RGB(255, 255, 255)
                                                  : RGB(90, 94, 100));
        HGDIOBJ oldPen = SelectObject(item->hDC, focus);
        HGDIOBJ oldBrush = SelectObject(item->hDC, GetStockObject(NULL_BRUSH));
        RoundRect(item->hDC, rect.left, rect.top, rect.right, rect.bottom,
                  DpiValue(6, dpi), DpiValue(6, dpi));
        SelectObject(item->hDC, oldBrush);
        SelectObject(item->hDC, oldPen);
        DeleteObject(focus);
    }
}

LRESULT CALLBACK WindowProc(HWND window, UINT message, WPARAM wParam, LPARAM lParam) {
    auto *state = reinterpret_cast<State *>(GetWindowLongPtrW(window, GWLP_USERDATA));
    if (message == WM_NCCREATE) {
        state = reinterpret_cast<State *>(reinterpret_cast<CREATESTRUCTW *>(lParam)->lpCreateParams);
        SetWindowLongPtrW(window, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(state));
    }
    switch (message) {
    case WM_CREATE: {
        const UINT dpi = GetDpiForWindow(window);
        state->font = CreateUiFont(dpi, 10, FW_NORMAL);
        state->titleFont = CreateUiFont(dpi, 18, FW_SEMIBOLD);
        state->semiboldFont = CreateUiFont(dpi, 10, FW_SEMIBOLD);
        state->backgroundBrush = CreateSolidBrush(RGB(245, 246, 248));
        state->cardBrush = CreateSolidBrush(RGB(255, 255, 255));
        state->editBrush = CreateSolidBrush(RGB(255, 255, 255));

        state->windowIcon = static_cast<HICON>(LoadImageW(
            GetModuleHandleW(nullptr), MAKEINTRESOURCEW(101), IMAGE_ICON,
            DpiValue(48, dpi), DpiValue(48, dpi), LR_DEFAULTCOLOR));
        SendMessageW(window, WM_SETICON, ICON_BIG,
                     reinterpret_cast<LPARAM>(state->windowIcon));
        SendMessageW(window, WM_SETICON, ICON_SMALL,
                     reinterpret_cast<LPARAM>(state->windowIcon));
        int cornerPreference = 2;
        DwmSetWindowAttribute(window, 33, &cornerPreference,
                              sizeof(cornerPreference));

        HWND title = CreateWindowW(L"STATIC", L"Mari 中文补丁",
            WS_CHILD | WS_VISIBLE, DpiValue(96, dpi), DpiValue(29, dpi),
            DpiValue(520, dpi), DpiValue(32, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kTitleLabel)), nullptr, nullptr);
        HWND subtitle = CreateWindowW(L"STATIC",
            L"独立启动，不替换原程序；支持高分屏与文件关联",
            WS_CHILD | WS_VISIBLE, DpiValue(96, dpi), DpiValue(64, dpi),
            DpiValue(520, dpi), DpiValue(24, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kSubtitleLabel)), nullptr, nullptr);
        HWND label = CreateWindowW(L"STATIC", L"安装位置",
            WS_CHILD | WS_VISIBLE, DpiValue(48, dpi), DpiValue(126, dpi),
            DpiValue(160, dpi), DpiValue(22, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kPathLabel)), nullptr, nullptr);
        state->directoryEdit = CreateWindowExW(0, L"EDIT",
            state->directory.c_str(), WS_CHILD | WS_VISIBLE | WS_TABSTOP | ES_AUTOHSCROLL,
            DpiValue(55, dpi), DpiValue(162, dpi), DpiValue(462, dpi), DpiValue(24, dpi),
            window, reinterpret_cast<HMENU>(static_cast<INT_PTR>(kDirectoryEdit)), nullptr, nullptr);
        SendMessageW(state->directoryEdit, EM_SETMARGINS, EC_LEFTMARGIN | EC_RIGHTMARGIN,
                     MAKELPARAM(DpiValue(10, dpi), DpiValue(10, dpi)));
        HWND browse = CreateWindowW(L"BUTTON", L"浏览…",
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_OWNERDRAW,
            DpiValue(536, dpi), DpiValue(157, dpi), DpiValue(96, dpi), DpiValue(34, dpi),
            window, reinterpret_cast<HMENU>(static_cast<INT_PTR>(kBrowseButton)), nullptr, nullptr);
        state->dpiCheck = CreateWindowW(L"BUTTON", L"启用 4K 屏优化", WS_CHILD | WS_VISIBLE |
            WS_TABSTOP | BS_AUTOCHECKBOX, DpiValue(48, dpi), DpiValue(235, dpi),
            DpiValue(185, dpi), DpiValue(26, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kDpiCheck)), nullptr, nullptr);
        SendMessageW(state->dpiCheck, BM_SETCHECK, BST_CHECKED, 0);
        HWND hint = CreateWindowW(L"STATIC",
            L"适用于 4K 或高 DPI 屏幕，默认缩放系数 1.75",
            WS_CHILD | WS_VISIBLE, DpiValue(48, dpi), DpiValue(270, dpi),
            DpiValue(390, dpi), DpiValue(22, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kDpiHintLabel)), nullptr, nullptr);
        HWND scaleLabel = CreateWindowW(L"STATIC", L"缩放系数",
            WS_CHILD | WS_VISIBLE | SS_RIGHT, DpiValue(428, dpi), DpiValue(237, dpi),
            DpiValue(100, dpi), DpiValue(22, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kScaleLabel)), nullptr, nullptr);
        state->scaleEdit = CreateWindowExW(0, L"EDIT", L"1.75",
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | ES_CENTER | ES_AUTOHSCROLL,
            DpiValue(546, dpi), DpiValue(236, dpi), DpiValue(60, dpi), DpiValue(22, dpi),
            window, reinterpret_cast<HMENU>(static_cast<INT_PTR>(kScaleEdit)), nullptr, nullptr);
        HWND install = CreateWindowW(L"BUTTON", L"安装汉化", WS_CHILD | WS_VISIBLE |
            WS_TABSTOP | BS_OWNERDRAW, DpiValue(352, dpi), DpiValue(338, dpi),
            DpiValue(132, dpi), DpiValue(40, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kInstallButton)), nullptr, nullptr);
        HWND uninstall = CreateWindowW(L"BUTTON", L"拆卸汉化", WS_CHILD | WS_VISIBLE |
            WS_TABSTOP | BS_OWNERDRAW, DpiValue(500, dpi), DpiValue(338, dpi),
            DpiValue(132, dpi), DpiValue(40, dpi), window,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(kUninstallButton)),
            nullptr, nullptr);
        for (HWND control : {subtitle, label, state->directoryEdit, browse,
                             state->dpiCheck, hint, scaleLabel, state->scaleEdit,
                             install, uninstall})
            SendMessageW(control, WM_SETFONT, reinterpret_cast<WPARAM>(state->font), TRUE);
        SendMessageW(title, WM_SETFONT, reinterpret_cast<WPARAM>(state->titleFont), TRUE);
        for (HWND control : {label, state->dpiCheck, scaleLabel})
            SendMessageW(control, WM_SETFONT,
                         reinterpret_cast<WPARAM>(state->semiboldFont), TRUE);
        return 0;
    }
    case WM_PAINT: {
        PAINTSTRUCT paint{};
        HDC dc = BeginPaint(window, &paint);
        RECT client{};
        GetClientRect(window, &client);
        FillRect(dc, &client, state->backgroundBrush);
        const UINT dpi = GetDpiForWindow(window);
        RECT pathCard{DpiValue(28, dpi), DpiValue(108, dpi),
                      DpiValue(652, dpi), DpiValue(211, dpi)};
        RECT dpiCard{DpiValue(28, dpi), DpiValue(218, dpi),
                     DpiValue(652, dpi), DpiValue(308, dpi)};
        FillRoundedRect(dc, pathCard, DpiValue(12, dpi), RGB(255, 255, 255));
        FillRoundedRect(dc, dpiCard, DpiValue(12, dpi), RGB(255, 255, 255));
        RECT pathInput{DpiValue(48, dpi), DpiValue(156, dpi),
                       DpiValue(524, dpi), DpiValue(192, dpi)};
        RECT scaleInput{DpiValue(539, dpi), DpiValue(230, dpi),
                        DpiValue(613, dpi), DpiValue(264, dpi)};
        FillRoundedRect(dc, pathInput, DpiValue(6, dpi), RGB(255, 255, 255));
        FillRoundedRect(dc, scaleInput, DpiValue(6, dpi), RGB(255, 255, 255));
        DrawRoundedOutline(dc, pathInput, DpiValue(6, dpi),
            GetFocus() == state->directoryEdit ? RGB(0, 103, 192)
                                                : RGB(142, 148, 157),
            DpiValue(GetFocus() == state->directoryEdit ? 2 : 1, dpi));
        DrawRoundedOutline(dc, scaleInput, DpiValue(6, dpi),
            GetFocus() == state->scaleEdit ? RGB(0, 103, 192)
                                            : RGB(142, 148, 157),
            DpiValue(GetFocus() == state->scaleEdit ? 2 : 1, dpi));
        HICON icon = reinterpret_cast<HICON>(SendMessageW(window, WM_GETICON,
                                                           ICON_BIG, 0));
        if (icon)
            DrawIconEx(dc, DpiValue(32, dpi), DpiValue(29, dpi), icon,
                       DpiValue(48, dpi), DpiValue(48, dpi), 0, nullptr, DI_NORMAL);
        EndPaint(window, &paint);
        return 0;
    }
    case WM_DRAWITEM:
        DrawModernButton(reinterpret_cast<DRAWITEMSTRUCT *>(lParam), *state);
        return TRUE;
    case WM_CTLCOLORSTATIC:
    case WM_CTLCOLORBTN: {
        HDC dc = reinterpret_cast<HDC>(wParam);
        HWND control = reinterpret_cast<HWND>(lParam);
        const int id = GetDlgCtrlID(control);
        SetBkMode(dc, TRANSPARENT);
        SetTextColor(dc, (id == kSubtitleLabel || id == kDpiHintLabel)
                         ? RGB(96, 101, 109) : RGB(32, 35, 40));
        if (id == kTitleLabel || id == kSubtitleLabel)
            return reinterpret_cast<LRESULT>(state->backgroundBrush);
        return reinterpret_cast<LRESULT>(state->cardBrush);
    }
    case WM_CTLCOLOREDIT: {
        HDC dc = reinterpret_cast<HDC>(wParam);
        SetBkColor(dc, RGB(255, 255, 255));
        SetTextColor(dc, RGB(32, 35, 40));
        return reinterpret_cast<LRESULT>(state->editBrush);
    }
    case WM_COMMAND: {
        const int id = LOWORD(wParam);
        if ((id == kDirectoryEdit || id == kScaleEdit) &&
            (HIWORD(wParam) == EN_SETFOCUS || HIWORD(wParam) == EN_KILLFOCUS)) {
            InvalidateRect(window, nullptr, FALSE);
            return 0;
        }
        if (id == kBrowseButton) {
            std::wstring selected = ControlText(state->directoryEdit);
            if (ChooseDirectory(selected)) SetWindowTextW(state->directoryEdit, selected.c_str());
            return 0;
        }
        if (id == kDpiCheck) {
            EnableWindow(state->scaleEdit,
                SendMessageW(state->dpiCheck, BM_GETCHECK, 0, 0) == BST_CHECKED);
            return 0;
        }
        if (id == kInstallButton || id == kUninstallButton) {
            state->directory = ControlText(state->directoryEdit);
            if (!HasMariExecutable(state->directory)) {
                MessageBoxW(window, L"请选择包含 Mari 主程序的 Bundle\\bin 目录。",
                            kTitle, MB_OK | MB_ICONERROR);
                return 0;
            }
            if (id == kInstallButton &&
                SendMessageW(state->dpiCheck, BM_GETCHECK, 0, 0) == BST_CHECKED &&
                !ValidScale(ControlText(state->scaleEdit))) {
                MessageBoxW(window, L"缩放系数必须是 1.0 到 3.0 之间的数字。",
                            kTitle, MB_OK | MB_ICONERROR);
                return 0;
            }
            state->dpiEnabled =
                SendMessageW(state->dpiCheck, BM_GETCHECK, 0, 0) == BST_CHECKED;
            state->scale = ControlText(state->scaleEdit);
            state->operation = id;
            DestroyWindow(window);
            return 0;
        }
        break;
    }
    case WM_DESTROY:
        if (state && state->font) DeleteObject(state->font);
        if (state && state->titleFont) DeleteObject(state->titleFont);
        if (state && state->semiboldFont) DeleteObject(state->semiboldFont);
        if (state && state->backgroundBrush) DeleteObject(state->backgroundBrush);
        if (state && state->cardBrush) DeleteObject(state->cardBrush);
        if (state && state->editBrush) DeleteObject(state->editBrush);
        if (state && state->windowIcon) DestroyIcon(state->windowIcon);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(window, message, wParam, lParam);
}

int ShowWindowUi(HINSTANCE instance, State &state) {
    const wchar_t *className = L"MariChineseInstallerWindow";
    WNDCLASSEXW windowClass{};
    windowClass.cbSize = sizeof(windowClass);
    windowClass.lpfnWndProc = WindowProc;
    windowClass.hInstance = instance;
    windowClass.hCursor = LoadCursorW(nullptr, MAKEINTRESOURCEW(32512));
    windowClass.hIcon = LoadIconW(instance, MAKEINTRESOURCEW(101));
    windowClass.hIconSm = windowClass.hIcon;
    windowClass.hbrBackground = reinterpret_cast<HBRUSH>(COLOR_WINDOW + 1);
    windowClass.lpszClassName = className;
    if (!RegisterClassExW(&windowClass) && GetLastError() != ERROR_CLASS_ALREADY_EXISTS)
        return 0;
    const UINT dpi = GetDpiForSystem();
    RECT rectangle{0, 0, DpiValue(680, dpi), DpiValue(406, dpi)};
    AdjustWindowRectExForDpi(&rectangle, WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU,
                             FALSE, WS_EX_DLGMODALFRAME, dpi);
    HWND window = CreateWindowExW(WS_EX_DLGMODALFRAME, className, kTitle,
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU, CW_USEDEFAULT, CW_USEDEFAULT,
        rectangle.right - rectangle.left, rectangle.bottom - rectangle.top,
        nullptr, nullptr, instance, &state);
    if (!window) return 0;
    POINT cursor{};
    GetCursorPos(&cursor);
    MONITORINFO monitorInfo{sizeof(monitorInfo)};
    const HMONITOR monitor = MonitorFromPoint(cursor, MONITOR_DEFAULTTONEAREST);
    if (GetMonitorInfoW(monitor, &monitorInfo)) {
        RECT windowRect{};
        GetWindowRect(window, &windowRect);
        const int width = windowRect.right - windowRect.left;
        const int height = windowRect.bottom - windowRect.top;
        const RECT &work = monitorInfo.rcWork;
        const int x = work.left + ((work.right - work.left) - width) / 2;
        const int y = work.top + ((work.bottom - work.top) - height) / 2;
        SetWindowPos(window, nullptr, x, y, 0, 0,
                     SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE);
    }
    ShowWindow(window, SW_SHOW);
    MSG message{};
    while (GetMessageW(&message, nullptr, 0, 0) > 0) {
        if (!IsDialogMessageW(window, &message)) {
            TranslateMessage(&message);
            DispatchMessageW(&message);
        }
    }
    return state.operation;
}

} // namespace

int APIENTRY wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int) {
    SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
    INITCOMMONCONTROLSEX controls{sizeof(controls), ICC_STANDARD_CLASSES};
    InitCommonControlsEx(&controls);
    CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
    State state;
    if (!LoadPayload(state)) {
        MessageBoxW(nullptr, L"安装程序数据不完整，请重新构建或下载。",
                    kTitle, MB_OK | MB_ICONERROR);
        CoUninitialize();
        return 1;
    }
    state.directory = FindDefaultDirectory();
    const int operation = ShowWindowUi(instance, state);
    if (!operation) {
        CoUninitialize();
        return 0;
    }
    const bool ok = operation == kInstallButton
        ? Install(state, state.dpiEnabled, state.scale) : Uninstall(state);
    MessageBoxW(nullptr,
        ok ? (operation == kInstallButton
            ? L"安装完成。\n\n请通过“Mari 中文版”快捷方式启动，或双击 .mri、.mra、.mnc 文件。"
            : L"汉化已拆卸，Mari 文件关联已恢复。")
           : (operation == kInstallButton ? L"安装失败。" : L"拆卸失败。"),
        kTitle, MB_OK | (ok ? MB_ICONINFORMATION : MB_ICONERROR));
    CoUninitialize();
    return ok ? 0 : 2;
}
