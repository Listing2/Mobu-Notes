# Scripts — Mobu Python

Mobu 2025 `pyfbsdk` 자동화·배치 스크립트. **실행은 Mobu 내부** — Cursor venv는 편집·autocomplete 전용.

---

## Inventory

| Path | What | Run |
|------|------|-----|
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
