@echo off
setlocal

set "ROOT=%~dp0..\.."
set "SRC=%~dp0"
set "OUT=%ROOT%\build\dpi-experiment"
set "QT=%ROOT%\third_party\qt5sdk"
if not exist "%QT%\lib\Qt5Widgets.lib" set "QT=C:\Qt512\5.12.0\msvc2017_64"
set "VCVARS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not exist "%QT%\lib\Qt5Widgets.lib" (
    echo [ERROR] Qt 5 x64 MSVC SDK not found.
    exit /b 1
)
if not exist "%VCVARS%" (
    echo [ERROR] Visual Studio 2022 Build Tools not found.
    exit /b 1
)
if exist "%OUT%" rmdir /s /q "%OUT%"
if exist "%OUT%" (
    echo [ERROR] Cannot clean %OUT%. Close Mari and try again.
    exit /b 1
)
mkdir "%OUT%"

call "%VCVARS%" >nul

cl /nologo /O2 /W4 /LD /EHsc /std:c++17 /Zc:__cplusplus /permissive- /utf-8 ^
   /I"%QT%\include" "%SRC%dpi_hook.cpp" ^
   /Fo"%OUT%\dpi_hook.obj" /Fe:"%OUT%\MariDpiVtableTest.dll" ^
   /link "%QT%\lib\Qt5Core.lib" "%QT%\lib\Qt5Gui.lib" ^
   "%QT%\lib\Qt5Widgets.lib" user32.lib
if errorlevel 1 exit /b 1

cl /nologo /O2 /W4 /EHsc /std:c++17 /permissive- /utf-8 ^
   "%SRC%dpi_launcher.cpp" /Fo"%OUT%\dpi_launcher.obj" ^
   /Fe:"%OUT%\MariDpiVtableLauncher.exe" ^
   /link /SUBSYSTEM:WINDOWS user32.lib
if errorlevel 1 exit /b 1

del /q "%OUT%\dpi_hook.obj" "%OUT%\dpi_launcher.obj" 2>nul

echo DPI experiment build complete: %OUT%
endlocal
