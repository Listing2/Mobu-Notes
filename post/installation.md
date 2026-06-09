# MotionBuilder 2025 — 설치 경로 (로컬)

이 PC 레지스트리·디스크 기준 경로. 다른 PC는 `InstallPath`가 다를 수 있다.

## 설치 루트

| 항목 | 경로 |
|------|------|
| **InstallPath** | `E:\AutoDesk\MotionBuilder\MotionBuilder 2025\` |
| 실행 파일 | `E:\AutoDesk\MotionBuilder\MotionBuilder 2025\bin\x64\motionbuilder.exe` |
| 레지스트리 | `HKLM\SOFTWARE\Autodesk\MotionBuilder\2025` → `InstallPath` |

## Mobu가 쓰는 주요 폴더

```text
MotionBuilder 2025\
├── bin\
│   ├── x64\
│   │   ├── motionbuilder.exe      ← 실행
│   │   └── python\
│   │       └── python.exe         ← Mobu 내장 Python (스크립트 실행)
│   └── config\
│       ├── PythonStartup\         ← Mobu 시작 시 자동 로드 (.py)
│       └── Scripts\               ← Tools → Python Tools 메뉴에 등록되는 스크립트
├── OpenRealitySDK\                ← C++ 플러그인 SDK
└── ...
```

### 역할 정리

| 폴더 | 용도 |
|------|------|
| `bin\config\PythonStartup` | Mobu **시작할 때마다** 실행되는 Python (단축키·툴 UI 등) — **임의 .py 넣지 말 것** |
| `bin\config\Scripts` | **Python Tools** 메뉴 스크립트 — `main()`이 파일 끝에 **무조건** 있으면 시작·로드 시 크래시 가능 |
| `bin\x64\python\python.exe` | Mobu가 실제로 돌리는 인터프리터 — **Cursor venv와 별개** |
| 본 저장소 `post/scripts/` | Git으로 관리하는 스크립트 원본 — Mobu에 **복사·심볼릭 링크·PYTHONPATH**로 연결 |

## 이 저장소 스크립트 → Mobu에 연결

### 방법 A — Scripts 폴더에 복사/링크 (단순)

```powershell
# 예: retargeter.py 하나 연결 (관리자 권한 필요할 수 있음)
$MobuScripts = "E:\AutoDesk\MotionBuilder\MotionBuilder 2025\bin\config\Scripts"
New-Item -ItemType SymbolicLink -Path "$MobuScripts\MyTool.py" `
  -Target "E:\Projects\Repositories\Mobu-Notes\post\scripts\MyTool.py"
```

### 방법 B — Python Editor에서 직접 실행 (Retargeter 권장)

`Window` → `Python Editor` → `Open` → `post/scripts/vendor/retargeter/retargeter.py` → Execute (F5).

upstream [Retargeter](https://github.com/eksod/Retargeter) 원본은 맨 아래 `main()`만 있어 **Scripts 폴더에 그대로 두면 Mobu가 안 켜질 수 있음**.  
본 저장소 vendor copy는 `if __name__ in ("__main__", "__builtin__"):` 로 감쌈 — Scripts에 넣을 때도 **vendor copy** 사용.

### 방법 C — Python Editor (기타 스크립트)

`post/scripts/` 아래 `.py` → Open → Execute.

### 방법 D — Mobu에서 Cursor로 실행 (선택)

[MotionBuilder Utils](external-tools.md#motionbuilder-utils-실행디버그) 확장: Cursor에서 **Ctrl+Enter**로 Mobu에 코드 전송·디버그 attach.

### 방법 E — vendor (GitHub 외부 repo)

외부 `.py`는 `post/scripts/vendor/` — [vendor/README.md](../scripts/vendor/README.md) (복사 / submodule / symlink).

## Cursor / Pylance 스텁 (편집 전용)

Mobu 안의 `pyfbsdk`는 **Mobu 프로세스 안에서만** import 가능하다.  
Cursor 자동완성은 **별도 venv + motionbuilder-stubs** 를 쓴다.

```powershell
cd post/scripts
.\setup-dev.ps1
```

또는:

```powershell
py -3 -m venv post/scripts/.venv
post/scripts/.venv/Scripts/python.exe -m pip install -r post/scripts/requirements-dev.txt
```

워크스페이스 `.vscode/settings.json` 이 venv 인터프리터를 가리킨다.  
Cursor에서 **Python: Select Interpreter** → `post/scripts/.venv/Scripts/python.exe` 확인.

## 다른 PC에서 InstallPath 찾기

```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Autodesk\MotionBuilder\2025" -ErrorAction SilentlyContinue |
  Select-Object InstallPath
```

## 관련

- [scripts/README.md](scripts/README.md) — 스크립트 규칙·목록
- [external-tools.md](external-tools.md) — 외부 도구·Retargeter 등
