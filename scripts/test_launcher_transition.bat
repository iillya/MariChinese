@echo off
setlocal
for %%I in ("%~dp0..") do set "ROOT=%%~fI"
if not exist "%ROOT%\build\tests" mkdir "%ROOT%\build\tests"
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
cl /nologo /O2 /MT /W4 /WX /EHsc /std:c++17 /utf-8 ^
   "%ROOT%\source\analysis\launcher_transition_test.cpp" ^
   /Fo"%ROOT%\build\tests\launcher_transition.obj" ^
   /Fe:"%ROOT%\build\tests\launcher_transition.exe" ^
   /link /SUBSYSTEM:CONSOLE user32.lib version.lib
if errorlevel 1 exit /b 1
"%ROOT%\build\tests\launcher_transition.exe"
exit /b %ERRORLEVEL%
