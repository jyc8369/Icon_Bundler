# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import os
import sys

from PyInstaller.utils.hooks import collect_submodules

if sys.platform == "darwin":
    from PyInstaller.building.osx import BUNDLE

ROOT = Path(SPECPATH).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
SIGNING_IDENTITY = os.environ.get("MACOS_SIGNING_IDENTITY") or None

hiddenimports = []
hiddenimports += collect_submodules("customtkinter")
hiddenimports += collect_submodules("darkdetect")
hiddenimports += collect_submodules("PIL")
hiddenimports += ["icon_bundler.i18n"]

a = Analysis(
    [str(ROOT / "src" / "icon_bundler" / "app.py")],
    pathex=[str(ROOT / "src")],
    binaries=[],
    datas=[(str(ROOT / "src" / "icon_bundler" / "locales"), "icon_bundler/locales")],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="IconBundler",
    icon=str(ASSET_DIR / "icon.ico") if IS_WINDOWS else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=SIGNING_IDENTITY,
    entitlements_file=None,
)

if IS_MACOS:
    app = BUNDLE(
        exe,
        name="IconBundler.app",
        icon=str(ASSET_DIR / "icon.icns"),
        bundle_identifier="com.iconbundler.app",
    )
