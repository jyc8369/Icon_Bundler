#!/bin/sh
set -eu
ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
cd "$ROOT_DIR"
command -v pyinstaller >/dev/null 2>&1 || { echo "PyInstaller is not installed. Install packaging/pyinstaller/requirements-build.txt first." >&2; exit 1; }
pyinstaller --noconfirm --clean --distpath build-output/dist --workpath build-output/work packaging/pyinstaller/icon_bundler.spec
