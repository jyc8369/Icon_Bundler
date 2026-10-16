@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "ROOT_DIR=%%~fI"
cd /d "%ROOT_DIR%"
where pyinstaller >nul 2>nul
if errorlevel 1 (
  echo PyInstaller가 설치되어 있지 않습니다. packaging\pyinstaller\requirements-build.txt를 먼저 설치하세요. 1>&2
  exit /b 1
)
pyinstaller --noconfirm --clean --distpath build-output\dist --workpath build-output\work packaging\pyinstaller\icon_bundler.spec
if errorlevel 1 exit /b %errorlevel%
