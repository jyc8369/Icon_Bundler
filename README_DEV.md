# Icon Bundler Developer Notes

This document is for developers or for anyone studying how the app is built.

## Project Overview

Icon Bundler is a `CustomTkinter` desktop app that converts raster images into icon files.

Current capabilities:

- Input: `PNG`, `JPG`, `JPEG`
- Output: `ICO`, `ICNS`
- Language toggle: `en`, `ko`
- Release packaging: PyInstaller on Windows and macOS

## Core Files

- `main.py`: GUI, image conversion logic, language restart logic
- `i18n.py`: text table for `en` and `ko`
- `release/build/icon_bundler.spec`: PyInstaller spec
- `release/build/build_macos.sh`: macOS build wrapper
- `release/build/build_windows.cmd`: Windows build wrapper
- `.github/workflows/release.yml`: release pipeline

## Image Conversion Logic

### Shared pipeline

The app uses a shared conversion function:

- open source image
- transpose according to EXIF
- convert to `RGBA`
- keep aspect ratio
- center the image on a transparent square canvas
- save using the selected output format

### ICO

ICO export uses these sizes:

- `16x16`
- `32x32`
- `48x48`
- `256x256`

The code keeps sizes in ascending order and stops before the first upscale.

### ICNS

ICNS export uses these sizes:

- `16x16`
- `32x32`
- `64x64`
- `128x128`
- `256x256`
- `512x512`

The app imports `PIL.IcnsImagePlugin` so Pillow registers ICNS save support.

## Language Handling

Language state is intentionally simple:

- supported values: `en`, `ko`
- default on first launch: `en`
- changing the language restarts the GUI process

Why restart:

- It guarantees the whole window is rebuilt with the new language.
- It avoids stale text in existing widgets.
- It makes language switching deterministic in packaged builds.

Language selection is passed through environment variables:

- `ICON_BUNDLER_LANGUAGE`
- `ICON_BUNDLER_SOURCE`

## Packaging

### Spec layout

The PyInstaller spec is written to run from `release/build`.

Important details:

- `ROOT = Path.cwd().resolve().parents[1]`
- `ICON_DIR = Path.cwd().resolve()`
- `i18n` is listed in `hiddenimports`
- Windows uses `icon.ico`
- macOS uses `icon.icns`
- macOS output is a `.app` bundle inside the zip archive

### Release workflow

The release workflow builds:

- Windows on `windows-latest`
- macOS arm64 on `macos-15`
- macOS x86_64 on `macos-15-intel`

Release artifacts are named like:

- `IconBundler-<version>-windows.zip`
- `IconBundler-<version>-macos-arm64.zip`
- `IconBundler-<version>-macos-x86_64.zip`

## Implementation Notes

- The app keeps the source image path in memory while the process is running.
- If a converted file already exists, the app asks before overwriting it.
- The UI uses a small amount of state and is rebuilt on language change rather than diff-updating widgets.
- `customtkinter.StringVar` is used for the text fields.

## Practical Constraints

- Windows packages should be built on Windows.
- macOS packages should be built on macOS.
- `ICNS` generation depends on Pillow's ICNS plugin support.
- Very small or damaged images may not convert cleanly.

