# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import sys

from PyInstaller.utils.hooks import collect_submodules

if sys.platform == "darwin":
    from PyInstaller.building.osx import BUNDLE


block_cipher = None
# PyInstaller executes spec files via exec(), so __file__ is not available here.
# The workflow runs from release/build, so two parents up is the repository root.
ROOT = Path.cwd().resolve().parents[1]
ICON_DIR = Path.cwd().resolve()
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"

hiddenimports = []
hiddenimports += collect_submodules("customtkinter")
hiddenimports += collect_submodules("darkdetect")
hiddenimports += collect_submodules("PIL")
hiddenimports += ["i18n"]


a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[],
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
    [],
    exclude_binaries=True,
    name="IconBundler",
    icon=str(ICON_DIR / "icon.ico") if IS_WINDOWS else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="IconBundler",
)

if IS_MACOS:
    app = BUNDLE(
        coll,
        name="IconBundler.app",
        icon=str(ICON_DIR / "icon.icns"),
        bundle_identifier="com.iconbundler.app",
    )
