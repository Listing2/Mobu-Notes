# Scripts — Mobu Python

Mobu 2025 `pyfbsdk` 자동화·배치 스크립트. **실행은 Mobu 내부** — Cursor venv는 편집·autocomplete 전용.

---

## Inventory

| Path | What | Run |
|------|------|-----|
| [noise_cleaner.py](noise_cleaner.py) | 선택한 CR 컨트롤 FCurve 구간 smoothing | Python Editor · 상단 설정값 수정 |
| [vendor/retargeter/retargeter.py](vendor/retargeter/retargeter.py) | [Retargeter](https://github.com/eksod/Retargeter) — FBX batch retarget | Python Editor · **vendor copy only** |
| [vendor/](vendor/README.md) | external GitHub repos | see vendor guide |

Tool catalog: [external-tools.md](../external-tools.md)

---

## Run in Mobu

| Method | |
|--------|---|
| Python Editor | `Window` → `Python Editor` → Open → Execute |
| Scripts menu | `bin\config\Scripts\` — [installation.md](../installation.md) |
| Cursor Utils | [MotionBuilder Utils](../external-tools.md#motionbuilder-utils-실행디버그) — Ctrl+Enter |

Path · stub · `setup-dev.ps1`: **[installation.md](../installation.md)** (single source)

---

## Conventions

- 파일명·식별자: ASCII · 주석: 한국어
- 스크립트 상단: Mobu version · 실행 방법

## Noise cleaner quick use

1. Plot to CR 이후 **소스 제거**.
2. Head / Wrist / Finger 등 CR 컨트롤 선택.
3. `noise_cleaner.py` 상단 `START_FRAME`, `END_FRAME`, `CHANNEL_MODE`, `STRENGTH` 수정.
4. Python Editor에서 Execute.
5. Play 확인 후 필요하면 strength를 낮춰 재실행.

## Template

```python
# Mobu 2025 — 설명 한 줄
# 실행: Window → Python Editor → Execute

from pyfbsdk import *  # noqa: F403

def main() -> None:
    pass

if __name__ in ("__main__", "__builtin__"):
    main()
```

---

## Links

- [installation.md](../installation.md) · [vendor/README.md](vendor/README.md)
- [retargeting-cleanup.md](../workflows/retargeting-cleanup.md)
