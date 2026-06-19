[English](#english) | [한국어](#korean)

<a name="english"></a>
# Icon Bundler - Developer Notes

This document summarizes the project structure and implementation points for Icon Bundler.

## Project overview

Icon Bundler is a `CustomTkinter` desktop application that converts raster source images into icon files.

Current scope:

- Input: `PNG`, `JPG`, `JPEG`
- Output: `ICO`, `ICNS`
- Language switching: `en`, `ko`
- Packaging: PyInstaller builds for Windows and macOS

## Core files

- `main.py`: GUI, image conversion logic, and immediate language refresh
- `i18n.py`: `en` and `ko` string table
- `release/build/icon_bundler.spec`: PyInstaller spec
- `release/build/build_macos.sh`: macOS build wrapper
- `release/build/build_windows.cmd`: Windows build wrapper
- `.github/workflows/release.yml`: release pipeline

## Image conversion flow

The app uses one shared conversion function for ICO and ICNS exports.

1. Open the source image.
2. Apply EXIF orientation correction.
3. Convert the image to `RGBA`.
4. Preserve the original aspect ratio.
5. Center the image on a transparent square canvas.
6. Save the result in the selected icon format.

### ICO export

ICO export uses these sizes:

- `16x16`
- `32x32`
- `48x48`
- `256x256`

### ICNS export

ICNS export uses these sizes:

- `16x16`
- `32x32`
- `64x64`
- `128x128`
- `256x256`
- `512x512`
- `1024x1024`

Pillow's ICNS save support is enabled by importing `PIL.IcnsImagePlugin`.

## Language handling

- Supported values: `en`, `ko`
- Default language on first launch: `en`
- Changing the language refreshes registered widget text in the current GUI process immediately

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

The selected output path still follows the conversion button the user presses, while the candidate list makes both destinations visible before conversion.

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
- Size selection without upscaling
- ICO and ICNS file creation from a generated PNG
- Unsupported source extensions
- Missing source files
- Output format and suffix mismatches

## Practical constraints

- Windows packages should be built on Windows.
- macOS packages should be built on macOS.
- ICNS generation depends on Pillow's ICNS plugin support.
- Very small or damaged images may not convert cleanly.

<a name="korean"></a>
# Icon Bundler - 개발자 노트

이 문서는 Icon Bundler의 구조와 구현 포인트를 개발자 기준으로 정리합니다.

## 프로젝트 개요

Icon Bundler는 `CustomTkinter` 기반 데스크톱 앱으로, 래스터 이미지를 아이콘 파일로 변환합니다.

현재 범위:

- 입력: `PNG`, `JPG`, `JPEG`
- 출력: `ICO`, `ICNS`
- 언어 전환: `en`, `ko`
- 배포: Windows/macOS용 PyInstaller 패키징

## 핵심 파일

- `main.py`: GUI, 이미지 변환 로직, 언어 즉시 갱신
- `i18n.py`: `en`, `ko` 문자열 테이블
- `release/build/icon_bundler.spec`: PyInstaller spec
- `release/build/build_macos.sh`: macOS 빌드 래퍼
- `release/build/build_windows.cmd`: Windows 빌드 래퍼
- `.github/workflows/release.yml`: 릴리스 파이프라인

## 이미지 변환 로직

앱은 ICO와 ICNS 내보내기에 같은 변환 함수를 사용합니다.

1. 원본 이미지를 엽니다.
2. EXIF 기준 회전을 보정합니다.
3. 이미지를 `RGBA`로 변환합니다.
4. 원본 비율을 유지합니다.
5. 투명한 정사각 캔버스 중앙에 배치합니다.
6. 선택한 아이콘 형식으로 저장합니다.

### ICO 내보내기

ICO 내보내기 크기:

- `16x16`
- `32x32`
- `48x48`
- `256x256`

### ICNS 내보내기

ICNS 내보내기 크기:

- `16x16`
- `32x32`
- `64x64`
- `128x128`
- `256x256`
- `512x512`
- `1024x1024`

`PIL.IcnsImagePlugin`을 직접 import해서 Pillow가 ICNS 저장을 인식하도록 합니다.

## 언어 처리

- 지원 값: `en`, `ko`
- 첫 실행 기본값: `en`
- 언어 변경 시 현재 GUI 프로세스에서 등록된 위젯 텍스트를 즉시 갱신합니다

즉시 갱신하는 이유:

- 언어 변경만을 위해 패키징된 실행 파일을 다시 실행하지 않아도 됩니다.
- 선택된 원본 이미지와 출력 미리보기를 같은 창에서 유지할 수 있습니다.
- 번역 대상 위젯을 한곳에 등록해 새 UI 텍스트도 일관되게 갱신할 수 있습니다.

초기 언어와 선택적 원본 경로는 환경변수에서 읽을 수 있습니다.

- `ICON_BUNDLER_LANGUAGE`
- `ICON_BUNDLER_SOURCE`

## 출력 미리보기

원본 이미지를 선택하면 앱은 가능한 출력 경로를 둘 다 보여 줍니다.

- ICO 출력 경로
- ICNS 출력 경로

실제 선택된 출력 경로는 사용자가 누른 변환 버튼을 따르며, 후보 목록은 변환 전에 두 경로를 모두 확인할 수 있게 해 줍니다.

## 패키징

### spec 구조

PyInstaller spec는 `release/build`에서 실행되도록 작성되어 있습니다.

중요한 점:

- `ROOT = Path.cwd().resolve().parents[1]`
- `ICON_DIR = Path.cwd().resolve()`
- `i18n`을 `hiddenimports`에 포함
- Windows는 `icon.ico`
- macOS는 `icon.icns`
- macOS 결과물은 zip 안의 `.app` 번들

### 릴리스 워크플로

릴리스 워크플로는 다음을 빌드합니다.

- Windows: `windows-latest`
- macOS arm64: `macos-15`
- macOS x86_64: `macos-15-intel`

릴리스 산출물 이름:

- `IconBundler-<version>-windows.zip`
- `IconBundler-<version>-macos-arm64.zip`
- `IconBundler-<version>-macos-x86_64.zip`

## 테스트

개발 의존성 설치:

```bash
pip install -r requirements-dev.txt
```

자동 변환 검사 실행:

```bash
pytest
```

테스트 범위:

- 큰 원본에 대한 ICNS `1024x1024` 크기 선택
- 업스케일 없는 크기 선택
- 생성한 PNG로 ICO/ICNS 파일 생성
- 지원하지 않는 원본 확장자
- 원본 파일 없음
- 출력 형식과 확장자 불일치

## 실무 제약

- Windows 패키지는 Windows에서 빌드해야 합니다.
- macOS 패키지는 macOS에서 빌드해야 합니다.
- `ICNS` 생성은 Pillow의 ICNS 플러그인 지원에 의존합니다.
- 너무 작거나 손상된 이미지는 변환에 실패할 수 있습니다.
