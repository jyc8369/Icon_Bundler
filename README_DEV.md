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
- Packaging: PyInstaller builds for Windows, macOS, and Linux

## Core files

- `src/icon_bundler/app.py`: GUI and immediate language refresh
- `src/icon_bundler/conversion.py`: ICO/ICNS conversion logic
- `src/icon_bundler/i18n.py`: locale loader and language selection
- `src/icon_bundler/locales/*.json`: translated strings, one file per language
- `packaging/pyinstaller/icon_bundler.spec`: PyInstaller spec
- `scripts/build/`: platform build wrappers
- `assets/`: application and platform icons
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

- Translation strings are stored in `src/icon_bundler/locales/<language>.json`, one file per language.
- `i18n.py` loads the JSON files and discovers the supported language codes from their filenames (`en`, `ja`, `ko`).
- Default language on first launch: `en`
- Every locale file must define the same translation keys and formatting placeholders.
- Changing the language refreshes registered widget text in the current GUI process immediately.

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

The PyInstaller spec lives in `packaging/pyinstaller`; build wrappers can be run from any current directory. They write temporary build files to `build-output/` and release archives to `release/artifacts/`.

Important details:

- `ROOT` is derived from PyInstaller's `SPECPATH`, so builds do not depend on the caller's working directory.
- Source modules live under `src/icon_bundler/`; platform icons live under `assets/`.
- Locale JSON files are copied to `icon_bundler/locales` in the packaged application.
- The spec includes the `icon_bundler.i18n` module as a hidden import.
- Windows uses `assets/icon.ico`; macOS uses `assets/icon.icns`.
- The macOS build creates a `.app` bundle containing a onefile executable; Windows and Linux create standalone onefile executables.
- Build wrappers write intermediate files to `build-output/`; the workflow writes release archives to `release/artifacts/`.

### Release workflow

The release workflow builds:

- Windows on `windows-latest`
- macOS arm64 on `macos-15`
- macOS x86_64 on `macos-15-intel`

Release artifacts are named like:

- `IconBundler-<version>-windows.zip`
- `IconBundler-<version>-macos-arm64.zip`
- `IconBundler-<version>-macos-x86_64.zip`
- `IconBundler-<version>-linux-x86_64.tar.gz`

Both macOS jobs sign with a Developer ID Application certificate, notarize the
app with Apple's `notarytool`, staple the ticket, and then create the release
ZIP. Configure these repository Actions secrets:

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_P12_PASSWORD`
- `MACOS_SIGNING_IDENTITY`
- `APPLE_API_KEY_P8`
- `APPLE_API_KEY_ID`
- `APPLE_API_ISSUER`

## Testing

Install development dependencies with:

```bash
pip install -r requirements-dev.txt
```

Run the automated conversion checks with:

```bash
pytest
```

Before running the tests or the app, install the runtime and development
dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

The GUI also requires Tk. On Debian/Ubuntu CI and development machines,
install it with `sudo apt-get install python3-tk`; Fedora uses
`sudo dnf install python3-tkinter`, and Arch Linux uses `sudo pacman -S tk`.
Windows Python installations should include **tcl/tk and IDLE**. On macOS,
the official python.org installer is the recommended starting point.

Run the source application with:

```bash
python main.py
```

## Platform verification

The release workflow performs these automated checks:

- Windows: builds the standalone executable and archives it in a `.zip`.
- macOS: builds the `.app` bundle and archives it with `ditto`.
- Linux: builds the standalone executable, verifies it exists, and archives it
  as `.tar.gz`.

Each platform still needs one GUI smoke test on a desktop session: start the
packaged app, open a PNG/JPG file, create an ICO and an ICNS file, and confirm
that the output files open successfully. CI does not attempt to automate this
interactive test because hosted runners do not provide a consistent desktop
session.

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
- 배포: Windows/macOS/Linux용 PyInstaller 패키징

## 핵심 파일

- `src/icon_bundler/app.py`: GUI와 언어 즉시 갱신
- `src/icon_bundler/conversion.py`: ICO/ICNS 변환 로직
- `src/icon_bundler/i18n.py`: 언어 파일 로더와 언어 선택
- `src/icon_bundler/locales/*.json`: 언어별 번역 문자열
- `packaging/pyinstaller/icon_bundler.spec`: PyInstaller spec
- `scripts/build/`: 운영체제별 빌드 스크립트
- `assets/`: 프로그램 및 플랫폼 아이콘
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

- 번역 문자열은 `src/icon_bundler/locales/<언어 코드>.json`에 언어별로 저장합니다.
- `i18n.py`가 JSON 파일을 읽고 파일명에서 지원 언어 코드(`en`, `ja`, `ko`)를 찾습니다.
- 첫 실행 기본값: `en`
- 모든 언어 파일은 같은 번역 키와 서식용 플레이스홀더를 제공해야 합니다.
- 언어를 변경하면 현재 GUI 프로세스에서 등록된 위젯 텍스트를 즉시 갱신합니다.

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

PyInstaller spec는 `packaging/pyinstaller`에 있으며 빌드 스크립트는 어느 디렉터리에서든 실행할 수 있습니다. 임시 빌드 파일은 `build-output/`, 배포 압축 파일은 `release/artifacts/`에 생성됩니다.

중요한 점:

- `ROOT`는 PyInstaller의 `SPECPATH`에서 계산하므로 빌드를 호출한 현재 디렉터리에 영향을 받지 않습니다.
- 앱 모듈은 `src/icon_bundler/`, 플랫폼 아이콘은 `assets/`에 있습니다.
- 언어별 JSON 파일은 패키지 안의 `icon_bundler/locales`로 복사됩니다.
- spec에서 `icon_bundler.i18n`을 hidden import로 지정합니다.
- Windows 아이콘은 `assets/icon.ico`, macOS 아이콘은 `assets/icon.icns`입니다.
- macOS는 onefile 실행 파일을 포함하는 `.app` 번들을 만들고, Windows와 Linux는 onefile 실행 파일을 만듭니다.
- 중간 빌드 파일은 `build-output/`, 릴리스 압축 파일은 `release/artifacts/`에 생성됩니다.

### 릴리스 워크플로

릴리스 워크플로는 다음을 빌드합니다.

- Windows: `windows-latest`
- macOS arm64: `macos-15`
- macOS x86_64: `macos-15-intel`
- Linux x86_64: `ubuntu-24.04`

릴리스 산출물 이름:

- `IconBundler-<version>-windows.zip`
- `IconBundler-<version>-macos-arm64.zip`
- `IconBundler-<version>-macos-x86_64.zip`
- `IconBundler-<version>-linux-x86_64.tar.gz`

두 macOS job은 Developer ID Application 인증서로 앱을 서명하고, Apple
`notarytool`로 공증한 뒤 티켓을 부착한 다음 릴리스 ZIP을 만듭니다. 저장소의
Actions Secrets에 다음 값을 등록해야 합니다.

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_P12_PASSWORD`
- `MACOS_SIGNING_IDENTITY`
- `APPLE_API_KEY_P8`
- `APPLE_API_KEY_ID`
- `APPLE_API_ISSUER`

Linux distribution decision:

- The first Linux release format is `.tar.gz`, containing the standalone `IconBundler` executable.
- Users extract the archive and run `IconBundler`.
- AppImage is a possible follow-up format after the first Linux release is validated; it is not part of the current release workflow.

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
- Windows 및 Linux 패키지는 PyInstaller onefile 실행 파일입니다.
- macOS 패키지는 onefile 실행 파일을 포함한 `.app` 번들입니다.
- Linux 패키지는 Ubuntu에서 빌드하며 `.tar.gz`에 `IconBundler` 실행 파일 하나를 담습니다.
- Linux 사용자는 압축을 푼 뒤 `IconBundler`를 실행합니다.
- AppImage는 첫 Linux 릴리스 검증 후 후속 배포 형식으로 검토합니다.
- `ICNS` 생성은 Pillow의 ICNS 플러그인 지원에 의존합니다.
- 너무 작거나 손상된 이미지는 변환에 실패할 수 있습니다.
