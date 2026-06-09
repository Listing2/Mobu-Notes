# 외부 도구 · 참고 저장소

Mobu 2025 리타게팅·클린업·Python 스크립트 작성에 쓸 만한 **외부 리소스** 정리.  
본 저장소에 코드를 vendoring하지 않고, 링크·도입 메모만 둔다.

## 우선순위 요약

| 우선 | 저장소 | 용도 |
|------|--------|------|
| ★★★ | [eksod/Retargeter](https://github.com/eksod/Retargeter) | FBX 폴더 **일괄 merge + retarget** |
| ★★★ | [Neill3d/OpenMoBu](https://github.com/Neill3d/OpenMoBu) | PythonScripts, HIK 템플릿, 플러그인 |
| ★★☆ | [motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/) | Cursor `pyfbsdk` 자동완성 — [설치](scripts/README.md#cursor--pylance-스텁) |
| ★★☆ | [MotionBuilder Utils (VS Code)](https://github.com/nils-soderman/vscode-motionbuilder-utils) | Cursor에서 Mobu **실행·디버그** |
| ★★☆ | [matthewkapfhammer/awesome-motionbuilder](https://github.com/matthewkapfhammer/awesome-motionbuilder) | 튜토리얼·repo 허브 |
| ★☆☆ | [alinen/MotionScriptTools](https://github.com/alinen/MotionScriptTools) | BVH/TRC, [발 스크립트 노트](https://alinen.github.io/MotionScriptTools/notes/MotionBuilderFootScripts.html) |
| ★☆☆ | [alex3dbros/MotionbuilderPublicTools](https://github.com/alex3dbros/MotionbuilderPublicTools) | 소규모 애니 Python 유틸 |
| — | [Neill3d/MoPlugs](https://github.com/Neill3d/MoPlugs) | OpenMoBu 확장 팩, 릴리스 오래됨 — 필요 플러그인 있을 때만 |
| — | [shotgunsoftware/tk-motionbuilder](https://github.com/shotgunsoftware/tk-motionbuilder) | Flow Production Tracking 파이프 — **스킵** (스튜디오 TD용) |

---

## eksod/Retargeter

**본인 워크플로 Phase 1~2 배치화에 가장 가깝다.**

| 항목 | 내용 |
|------|------|
| URL | https://github.com/eksod/Retargeter |
| 라이선스 | as-is (README DISCLAIMER) |
| 하는 일 | characterize된 **타겟** + FBX **폴더** → merge(namespace `merged`) → retarget → plot |
| 전제 | 타겟 characterize 완료 · Reach/Offset을 캐릭터에 저장 · 0프레임 **T-pose** (미 characterize 모션) |
| 한계 | Control Rig 클린업 · Skeleton bake · export는 **수동** ([retargeting-cleanup.md](workflows/retargeting-cleanup.md) Phase 4~6) |

### 도입 체크리스트

- [ ] `retargeter.py` 를 `post/scripts/vendor/` 또는 Mobu `bin\config\Scripts`에 배치
- [ ] 타겟 캐릭터 Retarget Reach/Offset 튜닝 후 캐릭터 저장
- [ ] 테스트 FBX 2~3개로 Match Source·스케일 확인
- [ ] 배치 결과 → Control Rig 클린업 파이프로 이어가기

### 실행

Mobu → `Window` → `Python Editor` → `retargeter.py` Open → Execute.

---

## Neill3d/OpenMoBu

| 항목 | 내용 |
|------|------|
| URL | https://github.com/Neill3d/OpenMoBu |
| 내용 | C++/Python 플러그인, `PythonScripts/`, `HIK_Characterization_Templates/`, Release 설치包 |
| 문서 | [Wiki](https://github.com/Neill3d/OpenMoBu/wiki), [GitBook](https://openmobu.gitbook.io/main) |
| 연관 | [MoBu Config App](https://github.com/Neill3d/MoBu_ConfigApp) — 플러그인·스크립트 경로 설정 |

### 도입 체크리스트

- [ ] Release 또는 `bin/`에서 Mobu 2025 호환 바이너리 확인
- [ ] `HIK_Characterization_Templates` — VRM/게임 캐 characterize 참고
- [ ] `PythonScripts/` — plot·씬 유틸 필요한 것만 골라 `post/scripts/`에 래핑

---

## alinen/MotionScriptTools

| 항목 | 내용 |
|------|------|
| URL | https://github.com/alinen/MotionScriptTools |
| 용도 | 모캡 **BVH/TRC** + Mobu `motion_builder/` 스크립트 |
| FBX 중심 파이프 | 당장 필수는 아님 |
| 참고 | [MotionBuilderFootScripts](https://alinen.github.io/MotionScriptTools/notes/MotionBuilderFootScripts.html) — foot sliding 아이디어 |

---

## alex3dbros/MotionbuilderPublicTools

| 항목 | 내용 |
|------|------|
| URL | https://github.com/alex3dbros/MotionbuilderPublicTools |
| 용도 | `Animation/` 모듈 등 Python 라이브러리 형태 |
| 설정 | 저장소 경로를 **환경 변수 PYTHONPATH** 또는 Mobu 스크립트 path에 추가 |

---

## awesome-motionbuilder

| 항목 | 내용 |
|------|------|
| URL | https://github.com/matthewkapfhammer/awesome-motionbuilder |
| 사이트 | https://matthewkapfhammer.github.io/awesome-motionbuilder/ |
| 용도 | 포럼, 튜토리얼, Git repo **큐레이션** — 위 repo 외 추가 탐색용 |

---

## Cursor / VS Code 연동

### pyfbsdk 스텁 (편집·자동완성)

| 항목 | 내용 |
|------|------|
| PyPI | [`motionbuilder-stubs==2025.*`](https://pypi.org/project/motionbuilder-stubs/) |
| 생성기 (참고) | [nils-soderman/pyfbsdk-stub-generator](https://github.com/nils-soderman/pyfbsdk-stub-generator) → [Codeberg motionbuilder-stubs](https://codeberg.org/nils-soderman/motionbuilder-stubs) |
| 본 저장소 | `post/scripts/.venv` + [`.vscode/settings.json`](../.vscode/settings.json) |

**주의:** 스텁 venv에서 `import pyfbsdk`는 실패한다. Mobu **밖**에서는 타입 정보만 제공.

### MotionBuilder Utils (실행·디버그)

| 항목 | 내용 |
|------|------|
| GitHub (archive) | https://github.com/nils-soderman/vscode-motionbuilder-utils |
| 최신 | https://codeberg.org/nils-soderman/vscode-motionbuilder-python |
| 기능 | Mobu에서 **Ctrl+Enter** 실행, breakpoint 디버그, SDK 문서 검색 |
| 설치 | Cursor Extensions에서 `MotionBuilder` 검색 또는 VSIX / Marketplace |

Mobu 실행 파일 경로: [installation.md](installation.md).

---

## 본인 파이프와의 연결

```text
[배치] Retargeter          → Phase 1~2 자동화
[수동] retargeting-cleanup → Phase 4~6 Control Rig · export
[참고] OpenMoBu            → characterize · plot 스크립트
[개발] stubs + Utils       → post/scripts/ 작성
[학습] awesome-motionbuilder · MotionScriptTools foot 노트
```

## TODO

- [ ] Retargeter를 `post/scripts/`에 fork·래핑할지 결정
- [ ] OpenMoBu Release 2025 호환 테스트
- [ ] MotionBuilder Utils 확장 설치·Mobu attach 확인
