@echo off
setlocal
set "ROOT=%~dp0.."
set "QT=%~1"
if not defined QT exit /b 2
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "OUT=%ROOT%\build\painter-bounds-acceptance"
if not exist "%OUT%" mkdir "%OUT%"
cl /nologo /EHsc /std:c++17 /Zc:__cplusplus /permissive- /O2 /W4 /WX /utf-8 /MD /DQT_NO_DEBUG ^
 /external:I"%QT%\include" /external:W0 "%ROOT%\source\analysis\painter_bounds_acceptance.cpp" ^
 /Fo"%OUT%\test.obj" /Fe:"%OUT%\test.exe" ^
 /link /LIBPATH:"%QT%\lib" Qt5Core.lib Qt5Gui.lib Qt5Widgets.lib user32.lib
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "PATH=%QT%\bin;%PATH%"
set "QT_PLUGIN_PATH=%QT%\plugins"
set "QT_QPA_PLATFORM=offscreen"
set "QT_QPA_FONTDIR=%WINDIR%\Fonts"
"%OUT%\test.exe" "%ROOT%\build\out\MariChineseHook.dll"
exit /b %errorlevel%
