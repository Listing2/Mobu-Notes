# MotionBuilder Python 스크립트

Mobu 2025 Python API(`pyfbsdk`)로 자동화·배치 처리 스크립트를 둡니다.

## 규칙

- 파일명·식별자: ASCII
- 주석: 한국어
- 스크립트 상단에 Mobu 버전·실행 방법(메뉴/단축키) 기록
- **실행은 Mobu 내부** — Cursor venv는 편집·자동완성 전용

## 목록

| 스크립트 | 설명 | 상태 |
|----------|------|------|
| (추가 예정) | | |
| [vendor/](vendor/README.md) | GitHub 외부 repo 추가·연결 |

외부 도구 카탈로그: [external-tools.md](../external-tools.md)

## Mobu에서 실행

| 방법 | 설명 |
|------|------|
| Python Editor | `Window` → `Python Editor` → Open → Execute |
| Scripts 메뉴 | `bin\config\Scripts\` — [installation.md](../installation.md) |
| Cursor Utils (선택) | [MotionBuilder Utils](../external-tools.md#motionbuilder-utils-실행디버그) — Ctrl+Enter |

## Cursor / 스텁 · Mobu 경로

InstallPath, Scripts 폴더, `setup-dev.ps1`, Pylance 스텁 — **[installation.md](../installation.md)** (단일 출처).

## 스크립트 템플릿

```python
# Mobu 2025 — 설명 한 줄
# 실행: Window → Python Editor → Execute / Scripts 메뉴

from pyfbsdk import *  # noqa: F403 — Mobu 내부 전용

def main() -> None:
    pass  # 본문

if __name__ in ("__main__", "__builtin__"):
    main()
```

## 관련

- [installation.md](../installation.md) — 경로·스텁·Mobu 연결
- [vendor/README.md](vendor/README.md) — GitHub 코드 추가
- [external-tools.md](../external-tools.md) — Retargeter, OpenMoBu
- [workflows/retargeting-cleanup.md](../workflows/retargeting-cleanup.md) — 수동 클린업 파이프
