@echo off
setlocal
set "ROOT=%~dp0.."
set "QT=%~1"
if not defined QT exit /b 2
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "OUT=%ROOT%\build\ui-paint-boundary-test"
if not exist "%OUT%" mkdir "%OUT%"
cl /nologo /EHsc /std:c++17 /Zc:__cplusplus /permissive- /O2 /W4 /WX /utf-8 /MD ^
 /I"%QT%\include" "%ROOT%\source\analysis\ui_paint_boundary_test.cpp" ^
 /Fo"%OUT%\test.obj" /Fe:"%OUT%\test.exe" /link /LIBPATH:"%QT%\lib" Qt5Core.lib Qt5Gui.lib Qt5Widgets.lib
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "PATH=%QT%\bin;%PATH%"
set "QT_QPA_PLATFORM=offscreen"
set "QT_PLUGIN_PATH=%QT%\plugins"
"%OUT%\test.exe"
exit /b %errorlevel%
