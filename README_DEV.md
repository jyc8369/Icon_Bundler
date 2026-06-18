# Icon Bundler - Developer Notes

<<<<<<< HEAD
This guide explains the project structure, conversion flow, localization behavior, packaging setup, and test workflow for developers working on Icon Bundler.

## Project overview

Icon Bundler is a `CustomTkinter` desktop application that converts raster source images into platform icon files.
=======
[English](README_DEV.md) | [한국어](README_DEV_KO.md)

이 문서는 Icon Bundler의 구조와 구현 포인트를 개발자 기준으로 정리합니다.

## 프로젝트 개요
>>>>>>> origin/main

Icon Bundler는 `CustomTkinter` 기반 데스크톱 앱으로, 래스터 이미지를 아이콘 파일로 변환합니다.

<<<<<<< HEAD
- Input formats: `PNG`, `JPG`, `JPEG`
- Output formats: `ICO`, `ICNS`
- Language options: `en`, `ko`
- Packaging target: PyInstaller builds for Windows and macOS

## Core files

- `main.py`: GUI, source validation, icon conversion, output preview handling, and in-place language refresh logic
- `i18n.py`: localized text table for English and Korean
- `requirements.txt`: runtime dependencies
- `requirements-dev.txt`: development and test dependencies
- `tests/test_conversion.py`: automated conversion and validation tests
- `release/build/icon_bundler.spec`: PyInstaller specification
- `release/build/build_macos.sh`: macOS build wrapper
- `release/build/build_windows.cmd`: Windows build wrapper
- `.github/workflows/release.yml`: release pipeline

## Image conversion flow

The app uses one shared conversion pipeline for ICO and ICNS exports:

1. Validate that the source path exists and has a supported extension.
2. Validate that the requested output format matches its expected suffix.
3. Open the source image with Pillow.
4. Apply EXIF-based orientation correction.
5. Convert the image to `RGBA`.
6. Preserve the original aspect ratio.
7. Center the image on a transparent square canvas.
8. Save the result with the selected icon format and size list.

### ICO export

ICO export uses these sizes, stopping before the first size larger than the source image:
=======
지원 범위:

- 입력: `PNG`, `JPG`, `JPEG`
- 출력: `ICO`, `ICNS`
- 언어 전환: `en`, `ko`
- 배포: Windows/macOS용 PyInstaller 패키징

## 핵심 파일

- `main.py`: GUI, 이미지 변환, 언어 전환
- `i18n.py`: `en`, `ko` 문자열 테이블
- `release/build/icon_bundler.spec`: PyInstaller spec
- `release/build/build_macos.sh`: macOS 빌드 스크립트
- `release/build/build_windows.cmd`: Windows 빌드 스크립트
- `.github/workflows/release.yml`: 릴리스 파이프라인

## 변환 로직

### 공통 파이프라인

- 원본 이미지 열기
- EXIF 방향 보정
- `RGBA` 변환
- 원본 비율 유지
- 투명한 정사각형 캔버스 중앙 배치
- 선택한 포맷으로 저장

### ICO
>>>>>>> origin/main

- `16x16`
- `32x32`
- `48x48`
- `256x256`

<<<<<<< HEAD
### ICNS export

ICNS export uses these sizes, stopping before the first size larger than the source image:
=======
### ICNS
>>>>>>> origin/main

- `16x16`
- `32x32`
- `64x64`
- `128x128`
- `256x256`
- `512x512`
- `1024x1024`

<<<<<<< HEAD
The app imports `PIL.IcnsImagePlugin` so Pillow registers ICNS save support before conversion.

## Validation and expected errors

Conversion failures that can be predicted are represented with explicit exception types:

- `MissingSourceError`: the selected source file no longer exists.
- `UnsupportedSourceError`: the selected source file extension is not supported.
- `UnsupportedOutputFormatError`: the requested format and file suffix do not match a supported output configuration.

The GUI maps these expected exceptions to localized messages before showing them to the user.

## Language handling
=======
## 언어 처리

- 지원 값은 `en`, `ko`다.
- 첫 실행 기본값은 `en`이다.
- 언어 변경 시 현재 창의 등록 위젯 텍스트를 즉시 갱신한다.
>>>>>>> origin/main

## 구현 시 주의사항

<<<<<<< HEAD
- Supported values: `en`, `ko`
- Default language on first launch: `en`
- Language changes refresh registered widget text in the current GUI process.

Why the app refreshes in place:

- It avoids launching a second packaged executable just to switch languages.
- It keeps the selected source image and output previews in the same window.
- It keeps translatable widgets in one registry so new UI labels and buttons can be refreshed consistently.

Initial language and an optional source path can still be read from environment variables:

- `ICON_BUNDLER_LANGUAGE`
- `ICON_BUNDLER_SOURCE`

## Output preview behavior

After a source image is selected, the app shows both possible output destinations:

- ICO output path
- ICNS output path

The currently selected output path still follows the conversion button the user presses, while the candidate list makes both destinations visible before conversion.

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

## Testing

Install development dependencies with:

```bash
pip install -r requirements-dev.txt
```

Run the automated conversion checks with:

```bash
pytest
```

The test suite covers:

- ICNS `1024x1024` size selection for large sources
- size selection without upscaling
- ICO and ICNS file creation from a generated PNG
- unsupported source extensions
- missing source files
- output format and suffix mismatches

## Practical constraints

- Windows packages should be built on Windows.
- macOS packages should be built on macOS.
- ICNS generation depends on Pillow's ICNS plugin support.
- Very small or damaged images may not convert cleanly.
=======
- 동일 이미지 경로를 실행 중 메모리에서 유지한다.
- 이미 존재하는 출력 파일은 덮어쓰기 전에 확인한다.
- UI는 언어 변경 시 등록된 요소를 다시 렌더링한다.
- `customtkinter.StringVar`를 사용한다.

## 테스트

```bash
pip install -r requirements-dev.txt
pytest
```

>>>>>>> origin/main
