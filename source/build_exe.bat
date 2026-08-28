@echo off
setlocal

set "PROJECT_DIR=%~dp0.."
set "WIX_DIR=%PROJECT_DIR%\build\wix314"
set "EXE_BUILD_DIR=%PROJECT_DIR%\build\bundle"
set "DIST_DIR=%PROJECT_DIR%\dist"

call "%~dp0build_msi.bat"
if errorlevel 1 exit /b 1
if not exist "%EXE_BUILD_DIR%" mkdir "%EXE_BUILD_DIR%"

"%WIX_DIR%\candle.exe" -nologo -arch x64 -ext WixBalExtension -dProjectDir="%PROJECT_DIR%" -out "%EXE_BUILD_DIR%\bundle.wixobj" "%~dp0bundle.wxs"
if errorlevel 1 exit /b 1

"%WIX_DIR%\light.exe" -nologo -ext WixBalExtension -out "%DIST_DIR%\MariChineseSetup.exe" "%EXE_BUILD_DIR%\bundle.wixobj"
if errorlevel 1 exit /b 1

echo Created "%DIST_DIR%\MariChineseSetup.exe"
endlocal
