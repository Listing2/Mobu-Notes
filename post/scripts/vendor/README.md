# vendor — 외부 GitHub 코드

[Retargeter](https://github.com/eksod/Retargeter), [OpenMoBu](https://github.com/Neill3d/OpenMoBu) PythonScripts 등 **외부 repo**를 이 저장소·Mobu에 붙이는 방법.

본인 작성 스크립트는 `post/scripts/` 루트, **외부에서 가져온 것**은 `post/scripts/vendor/<이름>/` 에 둔다.

```text
post/scripts/
├── setup-dev.ps1          ← Cursor 스텁 (Mobu 실행 X)
├── my_tool.py             ← 직접 작성
└── vendor/
    ├── README.md          ← 이 파일
    ├── retargeter/        ← 예: eksod/Retargeter 복사 또는 submodule
    └── openmobu/          ← 예: 필요한 .py만
```

---

## 방법 1 — 복사 (가장 단순, 권장 시작)

1. GitHub에서 **Release** 또는 `raw` `.py` 다운로드.
2. `post/scripts/vendor/<프로젝트명>/` 에 저장.
3. Mobu **Python Editor** → Open → Execute.

```powershell
# 예: Retargeter
New-Item -ItemType Directory -Force -Path "post/scripts/vendor/retargeter"
# retargeter.py 를 해당 폴더에 복사
```

| 장점 | 단점 |
|------|------|
| repo 독립, 버전 고정 | upstream 업데이트 시 수동 복사 |

**Mobu-Notes에 커밋할지:**  
- 라이선스 OK + 파일 적음 → vendor에 **커밋 가능** (Retargeter README에 as-is 명시).  
- 대형 repo 전체 → **커밋하지 말고** 로컬만 두거나 submodule.

---

## 방법 2 — git submodule (upstream 추적)

Mobu-Notes repo 안에서 외부 repo를 **링크**만 걸기.

```powershell
cd E:\Projects\Repositories\Mobu-Notes
git submodule add https://github.com/eksod/Retargeter.git post/scripts/vendor/retargeter
git submodule add https://github.com/Neill3d/OpenMoBu.git post/scripts/vendor/openmobu
```

| 장점 | 단점 |
|------|------|
| `git submodule update` 로 업데이트 | OpenMoBu 전체는 **용량·C++ 빌드** 큼 — PythonScripts만 쓸 거면 복사가 나을 수 있음 |
| clone 시 `--recurse-submodules` 필요 | |

OpenMoBu는 **Release/bin** 플러그인과 **PythonScripts/** 를 구분. Python만 쓸 때:

```powershell
git submodule add --depth 1 https://github.com/Neill3d/OpenMoBu.git post/scripts/vendor/openmobu
# 실행은 vendor/openmobu/PythonScripts/ 아래 개별 .py
```

---

## 방법 3 — Mobu Scripts 폴더에 심볼릭 링크

Mobu 메뉴 **Python Tools**에 바로 뜨게.

```powershell
$MobuScripts = "E:\AutoDesk\MotionBuilder\MotionBuilder 2025\bin\config\Scripts"
$Repo = "E:\Projects\Repositories\Mobu-Notes\post\scripts"

# 직접 작성 스크립트 1개
New-Item -ItemType SymbolicLink -Force `
  -Path "$MobuScripts\MobuNotes_MyTool.py" `
  -Target "$Repo\my_tool.py"

# vendor 스크립트 1개
New-Item -ItemType SymbolicLink -Force `
  -Path "$MobuScripts\Retargeter.py" `
  -Target "$Repo\vendor\retargeter\retargeter.py"
```

관리자 권한 필요할 수 있음. [installation.md](../../installation.md) 참고.

---

## 방법 4 — OpenMoBu 플러그인 (C++ / bin)

Python이 아닌 **플러그인**은 Scripts가 아니라 Mobu **플러그인 경로**.

1. [OpenMoBu Releases](https://github.com/Neill3d/OpenMoBu/releases) 에서 Mobu 2025용 설치包.
2. 또는 [MoBu Config App](https://github.com/Neill3d/MoBu_ConfigApp)으로 plugin/script path 등록.
3. `post/scripts/vendor/` 와 별개 — **문서만** [external-tools.md](../../external-tools.md)에 기록.

---

## Cursor에서 편집

| 대상 | Cursor |
|------|--------|
| `post/scripts/*.py`, `vendor/**/*.py` | [installation.md](../../installation.md#cursor--pylance-스텁-편집-전용) — venv + stubs |
| 실행 | Mobu Python Editor 또는 [MotionBuilder Utils](../../external-tools.md#motionbuilder-utils-실행디버그) |

vendor 코드를 **수정**하면 upstream과 diverge — 가능하면 **래퍼** `post/scripts/my_retargeter_run.py` 에서 import.

---

## 권장 도입 순서

| 순서 | repo | 넣는 위치 | Mobu에서 |
|------|------|-----------|----------|
| 1 | [Retargeter](https://github.com/eksod/Retargeter) | `vendor/retargeter/retargeter.py` | Python Editor → Execute |
| 2 | [MotionScriptTools](https://github.com/alinen/MotionScriptTools) `/motion_builder` | 필요 `.py`만 복사 | foot 등 |
| 3 | [OpenMoBu](https://github.com/Neill3d/OpenMoBu) | submodule 또는 Release 플러그인 | PythonScripts / bin |

전체 목록: [external-tools.md](../../external-tools.md). ML·실험: [ai-motion-cleanup.md](../../ai-motion-cleanup.md).

---

## Retargeter

[eksod/Retargeter](https://github.com/eksod/Retargeter) — characterize된 타겟 + FBX 폴더 → merge → retarget → plot.  
개요·한계: [external-tools.md](../../external-tools.md#eksodretargeter).

### 도입 체크리스트

- [ ] `retargeter.py` → `vendor/retargeter/` 또는 Mobu `bin\config\Scripts` (아래 방법 1~3)
- [ ] 타겟 Retarget Reach/Offset 튜닝 후 캐릭터 저장
- [ ] 테스트 FBX 2~3개로 Match Source·스케일 확인
- [ ] 배치 결과 → [retargeting-cleanup.md](../../workflows/retargeting-cleanup.md) Phase 4~6

### 실행

Mobu → `Window` → `Python Editor` → `vendor/retargeter/retargeter.py` Open → Execute.

---

## vendor 기록 (복붙용)

| 프로젝트 | URL | vendor 경로 | 라이선스 | Mobu 실행 |
|----------|-----|-------------|----------|-----------|
| Retargeter | https://github.com/eksod/Retargeter | `vendor/retargeter/` | as-is (README) | |
| OpenMoBu | https://github.com/Neill3d/OpenMoBu | `vendor/openmobu/` | repo LICENSE | |
| | | | | |

---

## .gitignore

- `post/scripts/.venv/` — 이미 ignore
- vendor **전체 clone**이 크면 submodule만 커밋하고 바이너리는 제외
- OpenMoBu `bin/` 은 **커밋하지 않음** — Release에서 설치

---

## 관련

- [../README.md](../README.md) — 스크립트 규칙·템플릿
- [../../installation.md](../../installation.md) — Mobu 경로·스텁
- [../../external-tools.md](../../external-tools.md) — 도구 카탈로그
