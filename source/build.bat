@echo off
setlocal
rem ===========================================================================
rem Mari Chinese Localizer - build script
rem Prereq: Visual Studio 2022 C++ build tools and a Qt 5 x64 MSVC SDK.
rem Output:
rem   build\out\*   intermediate binaries (hook DLL, launcher, runtime dict)
rem ===========================================================================

set "ROOT=%~dp0.."
set "CPP=%ROOT%\source"
set "OUT=%ROOT%\build\out"
set "OBJDIR=%ROOT%\build\obj"
set "ICONDIR=%ROOT%\icon"
rem QT5_BASELINE may point at the Qt 5.6.1 x64 MSVC SDK used for release builds.
rem Later Qt 5 SDKs remain useful for local checks, but cannot prove the minimum ABI.
set "QT=%QT5_BASELINE%"
if not exist "%QT%\lib\Qt5Widgets.lib" set "QT=%ROOT%\..\_ThirdParty\Qt\5.6.1\msvc2015_64"
if not exist "%QT%\lib\Qt5Widgets.lib" set "QT=%ROOT%\third_party\qt5sdk"
if not exist "%QT%\lib\Qt5Widgets.lib" (
    echo [ERROR] Qt 5 x64 MSVC SDK not found.
    echo Expected either %ROOT%\..\_ThirdParty\Qt\5.6.1\msvc2015_64 or %ROOT%\third_party\qt5sdk
    exit /b 1
)

if exist "%OUT%" rmdir /s /q "%OUT%"
if exist "%OBJDIR%" rmdir /s /q "%OBJDIR%"
if exist "%OUT%" (
    echo [ERROR] Cannot clean %OUT%. Close Mari and try again.
    exit /b 1
)
if exist "%OBJDIR%" (
    echo [ERROR] Cannot clean %OBJDIR%. Close build tools and try again.
    exit /b 1
)
mkdir "%OUT%"
mkdir "%OBJDIR%"

set "VCVARS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if not exist "%VCVARS%" (
    echo [ERROR] vcvars64.bat not found. Install VS2022 Build Tools.
    exit /b 1
)
call "%VCVARS%" >nul

echo === Compiling localization and DPI modules ===
cl /nologo /O2 /W4 /c /EHsc /std:c++17 /Zc:__cplusplus /permissive- /utf-8 ^
   /I"%QT%\include" ^
   "%CPP%\hook.cpp" ^
   /Fo"%OBJDIR%\hook.obj"
if errorlevel 1 exit /b 1

cl /nologo /O2 /W4 /c /EHsc /std:c++17 /Zc:__cplusplus /permissive- /utf-8 ^
   /I"%QT%\include" ^
   "%CPP%\dpi_hook.cpp" ^
   /Fo"%OBJDIR%\dpi_hook.obj"
if errorlevel 1 exit /b 1

echo === Linking unified hook DLL ===
link /nologo /DLL "%OBJDIR%\hook.obj" "%OBJDIR%\dpi_hook.obj" ^
   /OUT:"%OUT%\MariChineseHook.dll" ^
   /IMPLIB:"%OBJDIR%\MariChineseHook.lib" ^
   "%QT%\lib\Qt5Core.lib" "%QT%\lib\Qt5Gui.lib" "%QT%\lib\Qt5Widgets.lib" ^
   user32.lib shell32.lib psapi.lib
if errorlevel 1 exit /b 1

echo === Compiling launcher ===
rc /nologo /fo "%OBJDIR%\app_icon.res" "%ICONDIR%\app_icon.rc"
if errorlevel 1 exit /b 1
cl /nologo /O2 /W4 /EHsc /std:c++17 /permissive- /utf-8 ^
   "%CPP%\launcher.cpp" ^
   /Fo"%OBJDIR%\launcher.obj" ^
   "%OBJDIR%\app_icon.res" ^
   /Fe:"%OUT%\MariChineseLauncher.exe" ^
   /link /SUBSYSTEM:WINDOWS user32.lib
if errorlevel 1 exit /b 1

echo === Compiling installer ===
cl /nologo /O2 /W4 /EHsc /std:c++17 /permissive- /utf-8 ^
   "%CPP%\installer.cpp" ^
   /Fo"%OBJDIR%\installer.obj" ^
   "%OBJDIR%\app_icon.res" ^
   /Fe:"%OUT%\MariChineseInstaller.exe" ^
   /link /SUBSYSTEM:WINDOWS user32.lib shell32.lib ole32.lib advapi32.lib bcrypt.lib comctl32.lib gdi32.lib dwmapi.lib ^
   /MANIFEST:EMBED /MANIFESTUAC:"level='requireAdministrator' uiAccess='false'"
if errorlevel 1 exit /b 1

echo === Staging runtime dictionary ===
if not exist "%OUT%\translations" mkdir "%OUT%\translations"
copy /Y "%ROOT%\translations\dictionary_zh.json" "%OUT%\translations\dictionary_zh.json" >nul
if errorlevel 1 exit /b 1
copy /Y "%CPP%\settings.ini" "%OUT%\settings.ini" >nul
if errorlevel 1 exit /b 1

echo === Packing release installer ===
python "%CPP%\embed_files.py"
if errorlevel 1 exit /b 1

echo Build complete:
echo   %OUT%\MariChineseHook.dll
echo   %OUT%\MariChineseLauncher.exe
echo   %ROOT%\dist\MariChineseInstaller.exe
endlocal
