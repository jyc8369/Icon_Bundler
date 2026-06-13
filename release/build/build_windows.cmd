@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

where pyinstaller >nul 2>nul
if errorlevel 1 (
  echo PyInstaller가 설치되어 있지 않습니다. 먼저 의존성을 설치하세요. 1>&2
  exit /b 1
)

pyinstaller --noconfirm --clean icon_bundler.spec
if errorlevel 1 exit /b %errorlevel%
