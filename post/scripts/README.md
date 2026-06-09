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
| [외부] [Retargeter](https://github.com/eksod/Retargeter) | FBX 폴더 일괄 retarget | 도입 검토 — [external-tools.md](../external-tools.md) |

---

## Cursor / Pylance 스텁

Mobu 밖에서는 `pyfbsdk`를 import할 수 없다.  
Cursor에서 자동완성하려면 **[motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/)** 를 dev venv에 설치한다.

### 1회 설정

```powershell
cd post/scripts
.\setup-dev.ps1
```

### 수동

```powershell
py -3 -m venv post/scripts/.venv
post/scripts/.venv/Scripts/python.exe -m pip install -r post/scripts/requirements-dev.txt
```

### Cursor에서 확인

1. **Python: Select Interpreter** → `post/scripts/.venv/Scripts/python.exe`
2. `.vscode/settings.json` 이 워크스페이스에 적용됐는지 확인
3. `from pyfbsdk import *` 입력 시 Pylance 자동완성 동작

| 파일 | 역할 |
|------|------|
| `requirements-dev.txt` | `motionbuilder-stubs==2025.*` |
| `setup-dev.ps1` | venv 생성 + pip install |
| `.venv/` | gitignore — 로컬만 |

---

## Mobu에서 실행

| 방법 | 설명 |
|------|------|
| Python Editor | `Window` → `Python Editor` → Open → Execute |
| Scripts 메뉴 | `bin\config\Scripts\` 에 `.py` 배치 — [installation.md](../installation.md) |
| Cursor Utils (선택) | [MotionBuilder Utils](../external-tools.md#motionbuilder-utils-실행디버그) — Ctrl+Enter |

---

## Mobu 설치 경로 (이 PC)

| 항목 | 경로 |
|------|------|
| InstallPath | `E:\AutoDesk\MotionBuilder\MotionBuilder 2025\` |
| Python (Mobu) | `...\bin\x64\python\python.exe` |
| Scripts | `...\bin\config\Scripts\` |
| PythonStartup | `...\bin\config\PythonStartup\` |

상세: [installation.md](../installation.md)

---

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

---

## 관련

- [installation.md](../installation.md) — 폴더 구조·Mobu 연결
- [external-tools.md](../external-tools.md) — Retargeter, OpenMoBu, Utils
- [workflows/retargeting-cleanup.md](../workflows/retargeting-cleanup.md) — 수동 클린업 파이프
