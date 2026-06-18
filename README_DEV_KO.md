# Icon Bundler - 개발자 노트

[English](README_DEV.md) | [한국어](README_DEV_KO.md)

이 문서는 Icon Bundler의 구조와 구현 포인트를 개발자 기준으로 정리합니다.

## 프로젝트 개요

Icon Bundler는 `CustomTkinter` 기반 데스크톱 앱으로, 래스터 이미지를 아이콘 파일로 변환합니다.

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

- `16x16`
- `32x32`
- `48x48`
- `256x256`

### ICNS

- `16x16`
- `32x32`
- `64x64`
- `128x128`
- `256x256`
- `512x512`
- `1024x1024`

## 언어 처리

- 지원 값은 `en`, `ko`다.
- 첫 실행 기본값은 `en`이다.
- 언어 변경 시 현재 창의 등록 위젯 텍스트를 즉시 갱신한다.

## 구현 시 주의사항

- 동일 이미지 경로를 실행 중 메모리에서 유지한다.
- 이미 존재하는 출력 파일은 덮어쓰기 전에 확인한다.
- UI는 언어 변경 시 등록된 요소를 다시 렌더링한다.
- `customtkinter.StringVar`를 사용한다.

## 테스트

```bash
pip install -r requirements-dev.txt
pytest
```

