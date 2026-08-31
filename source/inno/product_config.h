#pragma once
#include <vector>
#include <string>
inline constexpr wchar_t kProductId[] = L"MariChinese";
inline constexpr wchar_t kHostPattern[] = L"Mari*.exe";
inline constexpr wchar_t kLauncher[] = L"MariChineseLauncher.exe";
inline const std::vector<const wchar_t*> kKnownHandlers = {};
inline const std::vector<const wchar_t*> kExtensions = {L".mri",L".mra",L".mnc"};
inline const std::vector<const wchar_t*> kLegacyHandlers = {L"MariChinese.mri",L"MariChinese.mra",L"MariChinese.mnc"};
inline const std::vector<const wchar_t*> kQtModules = {L"Core",L"Gui",L"Widgets"};
inline const std::vector<std::vector<DWORD>> kQtVersions = {{5,6,1}};
