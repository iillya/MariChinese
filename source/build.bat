@echo off
setlocal
rem ===========================================================================
rem Mari Chinese Localizer - build script
rem Prereq: Visual Studio 2022 C++ build tools, and Qt 5.15.2 MSVC x64 SDK
rem         under third_party\qt515sdk\5.15.2\msvc2019_64 (aqtinstall qtbase).
rem Output:
rem   build\out\*   intermediate binaries (hook DLL, launcher, runtime dict)
rem ===========================================================================

set "ROOT=%~dp0.."
set "CPP=%ROOT%\source"
set "OUT=%ROOT%\build\out"
set "OBJDIR=%ROOT%\build\obj"
set "QT=%ROOT%\third_party\qt515sdk\5.15.2\msvc2019_64"
if not exist "%OUT%" mkdir "%OUT%"
if not exist "%OBJDIR%" mkdir "%OBJDIR%"

if not exist "%QT%\lib\Qt5Widgets.lib" (
    echo [ERROR] Qt 5.15.2 SDK not found at %QT%
    exit /b 1
)

set "VCVARS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if not exist "%VCVARS%" (
    echo [ERROR] vcvars64.bat not found. Install VS2022 Build Tools.
    exit /b 1
)
call "%VCVARS%" >nul

echo === Compiling hook DLL ===
cl /nologo /O2 /W3 /LD /EHsc /std:c++17 /Zc:__cplusplus /permissive- /utf-8 ^
   /I"%QT%\include" ^
   "%CPP%\hook.cpp" ^
   /Fo"%OBJDIR%\hook.obj" ^
   /Fe:"%OUT%\MariChineseHook.dll" ^
   /link /IMPLIB:"%OBJDIR%\MariChineseHook.lib" ^
   "%QT%\lib\Qt5Core.lib" "%QT%\lib\Qt5Gui.lib" "%QT%\lib\Qt5Widgets.lib" ^
   user32.lib shell32.lib psapi.lib version.lib
if errorlevel 1 exit /b 1

echo === Compiling launcher ===
cl /nologo /O2 /W3 /EHsc /utf-8 ^
   "%CPP%\launcher.cpp" ^
   /Fo"%OBJDIR%\launcher.obj" ^
   /Fe:"%OUT%\MariChineseLauncher.exe" ^
   /link /SUBSYSTEM:WINDOWS user32.lib
if errorlevel 1 exit /b 1

echo === Staging runtime dictionary ===
if not exist "%OUT%\translations" mkdir "%OUT%\translations"
copy /Y "%ROOT%\translations\dictionary_zh.json" "%OUT%\translations\dictionary_zh.json" >nul

echo Build complete:
echo   %OUT%\MariChineseHook.dll
echo   %OUT%\MariChineseLauncher.exe
endlocal
