@echo off
setlocal

set "PROJECT_DIR=%~dp0.."
set "WIX_DIR=%PROJECT_DIR%\build\wix314"
set "PAYLOAD_DIR=%PROJECT_DIR%\build\out"
set "MSI_BUILD_DIR=%PROJECT_DIR%\build\msi"
set "DIST_DIR=%PROJECT_DIR%\dist"

if not exist "%WIX_DIR%\candle.exe" (
  echo WiX Toolset was not found at "%WIX_DIR%".
  exit /b 1
)

if not exist "%PAYLOAD_DIR%\MariChineseLauncher.exe" (
  echo Build the launcher and hook first by running source\build.bat.
  exit /b 1
)

if not exist "%MSI_BUILD_DIR%" mkdir "%MSI_BUILD_DIR%"
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

"%WIX_DIR%\candle.exe" -nologo -arch x64 -dProjectDir="%PROJECT_DIR%" -dPayloadDir="%PAYLOAD_DIR%" -out "%MSI_BUILD_DIR%\installer.wixobj" "%~dp0installer.wxs"
if errorlevel 1 exit /b 1

"%WIX_DIR%\light.exe" -nologo -out "%DIST_DIR%\MariChineseSetup.msi" "%MSI_BUILD_DIR%\installer.wixobj"
if errorlevel 1 exit /b 1

echo Created "%DIST_DIR%\MariChineseSetup.msi"
endlocal
