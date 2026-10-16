[English](#english) | [한국어](#korean)


<a name="english"></a>
# Icon Bundler

Icon Bundler turns a picture into an icon file.
You can use it to make `ICO` files for Windows or `ICNS` files for macOS.

## What it does

- Opens a `PNG`, `JPG`, or `JPEG` image
- Makes a Windows `ICO` file
- Makes a macOS `ICNS` file
- Keeps the picture centered and clean

## How to use

1. Download the version that matches your computer.
   - Windows: `.zip`
   - macOS: `.zip` containing the `.app`
   - Linux: `.tar.gz`
2. Open the app.
3. Select an image.
4. Click the icon format you want.
5. Save the output file.

## Running from source

Python 3.12 or newer is recommended. Install the dependencies first:

```bash
python -m pip install -r requirements.txt
```

Tk is required by the desktop file dialog. If Python reports that `tkinter` is
missing, install the platform package below and try again:

- Windows: reinstall Python from python.org with **tcl/tk and IDLE** selected.
- macOS: use the official python.org installer, or install Tcl/Tk with Homebrew.
- Debian/Ubuntu: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch Linux: `sudo pacman -S tk`

Start the app with:

```bash
python main.py
```

For a downloaded package, extract it first. On Linux run `IconBundler`; on
macOS open the `.app`; on Windows run `IconBundler.exe`.

## Notes

- The app keeps the picture size balanced.
- If a file with the same name already exists, it asks before replacing it.
- More details are in the developer guide.


[English](#english) | [한국어](#korean)


<a name="korean"></a>
# Icon Bundler


Icon Bundler는 사진을 아이콘 파일로 바꿔 주는 프로그램입니다.
Windows용 `ICO` 파일이나 macOS용 `ICNS` 파일을 만들 수 있습니다.

## 할 수 있는 일

- `PNG`, `JPG`, `JPEG` 파일 열기
- Windows용 `ICO` 만들기
- macOS용 `ICNS` 만들기
- 사진을 가운데에 맞춰 보기 좋게 처리하기

## 사용 방법

1. 내 컴퓨터에 맞는 버전을 다운로드합니다.
   - Windows: `.zip`
   - macOS: `.app`가 포함된 `.zip`
   - Linux: `.tar.gz`
2. 프로그램을 엽니다.
3. 이미지를 선택합니다.
4. 원하는 아이콘 형식을 누릅니다.
5. 결과 파일을 저장합니다.

## 참고

- 사진 크기를 보기 좋게 맞춰 줍니다.
- 같은 이름의 파일이 있으면 덮어쓸지 먼저 물어봅니다.
- 자세한 설명은 개발자 문서를 보세요.

## 소스에서 실행하기

Python 3.12 이상을 권장합니다. 먼저 의존성을 설치합니다.

```bash
python -m pip install -r requirements.txt
```

파일 선택 창에 필요한 Tk가 없다는 오류가 나오면 운영체제에 맞게
다음 항목을 설치하세요.

- Windows: python.org 설치 프로그램에서 **tcl/tk and IDLE** 선택
- macOS: 공식 python.org 설치 프로그램 사용 또는 Homebrew로 Tcl/Tk 설치
- Debian/Ubuntu: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch Linux: `sudo pacman -S tk`

실행:

```bash
python main.py
```

다운로드한 패키지는 먼저 압축을 풉니다. Linux는 `IconBundler`,
macOS는 `.app`, Windows는 `IconBundler.exe`를 실행합니다.
