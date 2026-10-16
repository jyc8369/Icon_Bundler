# Development

This guide covers verified source, build, test, packaging, and release procedures for Icon Bundler. End-user instructions are in the root [README](../README.md).

## Project layout

- `main.py`: source-checkout launcher; adds `src/` to the Python path.
- `src/icon_bundler/app.py`: CustomTkinter desktop interface.
- `src/icon_bundler/conversion.py`: image validation and ICO/ICNS conversion.
- `src/icon_bundler/i18n.py` and `src/icon_bundler/locales/`: locale loading and English, Japanese, and Korean strings.
- `tests/test_conversion.py`: conversion checks.
- `packaging/pyinstaller/icon_bundler.spec`: onefile packaging configuration.
- `scripts/build/`: operating-system build wrappers.
- `.github/workflows/release.yml`: tag-triggered build and release workflow.

## Development environment

The release workflow uses Python 3.12. Install application and test dependencies with:

```bash
python -m pip install -r requirements-dev.txt
```

The desktop interface uses Tk. Linux development environments may need the operating-system Tk package; the release workflow installs `python3-tk` on Ubuntu. The GUI requires a desktop session to run interactively.

## Run from source

```bash
python main.py
```

## Tests

```bash
pytest
```

The current automated checks cover ICNS size selection, avoiding upscaling where possible, ICO and ICNS creation, unsupported source extensions, missing source files, and output format/suffix mismatches. They do not automate an interactive GUI smoke test.

## Build packages

Install the build dependency after installing the application dependencies:

```bash
python -m pip install -r packaging/pyinstaller/requirements-build.txt
```

Run the wrapper for the build host:

```bash
scripts/build/build_linux.sh
```

On macOS use `scripts/build/build_macos.sh`; on Windows use `scripts\build\build_windows.cmd` from Command Prompt. The wrappers invoke `packaging/pyinstaller/icon_bundler.spec` and write PyInstaller output under `build-output/`. Build for the target operating system; the GitHub workflow uses separate Windows, macOS arm64, macOS x86_64, and Ubuntu x86_64 runners.

The spec produces a standalone onefile executable. On macOS, it is placed inside `IconBundler.app`. The release workflow packages the outputs as:

- `IconBundler-<version>-windows.zip`
- `IconBundler-<version>-macos-arm64.zip`
- `IconBundler-<version>-macos-x86_64.zip`
- `IconBundler-<version>-linux-x86_64.tar.gz`

The Linux archive contains the `IconBundler` executable. Build output is staged under `release/artifacts/` in the workflow.

## Release and macOS notarization

The workflow runs when a `v*` tag is pushed. It builds each platform artifact and creates a GitHub Release after all four build jobs succeed. The macOS jobs sign the app, submit it to Apple for notarization, poll the submission status, staple and validate the ticket, and then create the ZIP archive.

The macOS jobs read these repository Actions secrets:

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_P12_PASSWORD`
- `MACOS_SIGNING_IDENTITY`
- `APPLE_API_KEY_P8`
- `APPLE_API_KEY_ID`
- `APPLE_API_ISSUER`

The notarization helper is `scripts/notarize_macos.sh`. It separates submission from status polling, reports Apple's rejection log for rejected submissions, retries recognized transient network errors while reusing the submission ID, and records the ID in the job summary. Stapler validation is attempted up to three times in the workflow.

## Conversion details

The converter applies EXIF orientation, converts to RGBA, preserves the image aspect ratio, and centers it on a transparent square canvas. ICO output includes sizes from 16 through 256 pixels; ICNS output includes sizes from 16 through 1024 pixels. The converter selects sizes that do not exceed the source's smaller dimension when possible.

Locale files are JSON files in `src/icon_bundler/locales/`. `i18n.py` discovers supported languages from their filenames. Locale files should keep the same translation keys and formatting placeholders.
