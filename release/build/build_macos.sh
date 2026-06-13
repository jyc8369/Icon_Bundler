#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller가 설치되어 있지 않습니다. 먼저 의존성을 설치하세요." >&2
  exit 1
fi

pyinstaller --noconfirm --clean icon_bundler.spec
