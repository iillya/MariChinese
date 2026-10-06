@echo off
setlocal
set "ROOT=%~dp0.."
set "QT=%~1"
if not defined QT exit /b 2
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "OUT=%ROOT%\build\translation-lookup-test"
if not exist "%OUT%" mkdir "%OUT%"
cl /nologo /EHsc /std:c++17 /Zc:__cplusplus /permissive- /O2 /W4 /WX /utf-8 /MD ^
 /I"%QT%\include" /c "%ROOT%\source\analysis\translation_lookup_test.cpp" ^
 /Fo"%OUT%\test.obj"
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
cl /nologo /EHsc /std:c++17 /Zc:__cplusplus /permissive- /O2 /W4 /WX /utf-8 /MD ^
 /I"%QT%\include" /c "%ROOT%\source\translation_lookup.cpp" ^
 /Fo"%OUT%\translation_lookup.obj"
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
link /nologo "%OUT%\test.obj" "%OUT%\translation_lookup.obj" ^
 /OUT:"%OUT%\test.exe" /LIBPATH:"%QT%\lib" Qt5Core.lib
if errorlevel 1 exit /b 1
if not errorlevel 0 exit /b 1
set "PATH=%QT%\bin;%PATH%"
"%OUT%\test.exe"
exit /b %errorlevel%
