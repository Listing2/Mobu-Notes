# 외부 도구 · 참고 저장소

Mobu 2025 리타게팅·클린업·Python 스크립트 작성에 쓸 만한 **외부 리소스** 정리.  
본 저장소에 코드를 vendoring하지 않고, 링크·도입 메모만 둔다.

**AI · ML 클린업 옵션:** [ai-motion-cleanup.md](ai-motion-cleanup.md)

**GitHub 코드 추가:** [scripts/vendor/README.md](scripts/vendor/README.md)

## 우선순위 요약

| 우선 | 저장소 | 용도 |
|------|--------|------|
| ★★★ | [eksod/Retargeter](https://github.com/eksod/Retargeter) | FBX 폴더 **일괄 merge + retarget** |
| ★★★ | [Neill3d/OpenMoBu](https://github.com/Neill3d/OpenMoBu) | PythonScripts, HIK 템플릿, 플러그인 |
| ★★☆ | [motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/) | Cursor `pyfbsdk` 자동완성 — [설치](installation.md#cursor--pylance-스텁-편집-전용) |
| ★★☆ | [MotionBuilder Utils (VS Code)](https://github.com/nils-soderman/vscode-motionbuilder-utils) | Cursor에서 Mobu **실행·디버그** |
| ★★☆ | [matthewkapfhammer/awesome-motionbuilder](https://github.com/matthewkapfhammer/awesome-motionbuilder) | 튜토리얼·repo **허브** — [§ awesome](#awesome-motionbuilder) |
| ★☆☆ | [alinen/MotionScriptTools](https://github.com/alinen/MotionScriptTools) | BVH/TRC, [발 스크립트 노트](https://alinen.github.io/MotionScriptTools/notes/MotionBuilderFootScripts.html) |
| ★☆☆ | [eksod/additiveAnimation](https://github.com/eksod/additiveAnimation) | additive·레이어 개념 — [layer-override](workflows/layer-override-hands-head.md) 참고 |
| ★☆☆ | [ebadier/MotionBuilder-Tools](https://github.com/ebadier/MotionBuilder-Tools) | 씬·애니 Python 유틸 모음 — 필요 `.py`만 vendor |
| ★☆☆ | [alex3dbros/MotionbuilderPublicTools](https://github.com/alex3dbros/MotionbuilderPublicTools) | 소규모 애니 Python 라이브러리 |
| ★☆☆ | [SoerenFrohne/MotionBuilder-Pipeline-Scripts](https://github.com/SoerenFrohne/MotionBuilder-Pipeline-Scripts) | 클립·캐릭터 **배치** 파이프 스크립트 |
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

**도입·실행:** [scripts/vendor/README.md](scripts/vendor/README.md#retargeter)

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
### OpenMoBu — post에서 자주 쓸 PythonScripts

| 스크립트 | 용도 | 본인 Phase |
|----------|------|------------|
| `ReCreateRig.py` | Skeleton plot → CR 재생성 → CR에 plot | Retargeter **후** Phase 3 단축 |
| `StayOnFloor_2013.py` | 발 TRS hold — sliding 1차 | Phase 4.1 보조 |
| `FinalizeOnSkeleton.py` | Skeleton plot + CR 제거 | Phase 5~6 직전 |
| `CharTimeToZero.py` | 타임라인 0프레임 정렬 | Phase 0 |
| `BVH_Tool.py` | BVH import/export | Retargeter `.bvh` 경로와 병행 |

경로: repo `PythonScripts/Actions/Animation/` 등 — [ReadMe](https://github.com/Neill3d/OpenMoBu/blob/main/PythonScripts/ReadMe.md)

---

## alinen/MotionScriptTools

| 항목 | 내용 |
|------|------|
| URL | https://github.com/alinen/MotionScriptTools |
| 용도 | 모캡 **BVH/TRC** + Mobu `motion_builder/` 스크립트 |
| FBX 중심 파이프 | 당장 필수는 아님 |
| 참고 | [MotionBuilderFootScripts](https://alinen.github.io/MotionScriptTools/notes/MotionBuilderFootScripts.html) — foot sliding 아이디어 |
| 스크립트 | [`motion_builder/`](https://github.com/alinen/MotionScriptTools/tree/master/motion_builder) — ToesToFloor 등, 필요 파일만 vendor |

---

## eksod/additiveAnimation

Retargeter와 **동일作者**. take 간·레이어 간 **additive** 계산 로직.

| 항목 | 내용 |
|------|------|
| URL | https://github.com/eksod/additiveAnimation |
| 용도 | 베이스 take에서 차분 레이어 추출·적용 — Animation Layer + Weight와 **개념적으로 연결** |
| 본인 파이프 | [layer-override-hands-head.md](workflows/layer-override-hands-head.md) (손·머리 Weight) · OpenMoBu `libAdditiveAnimation.py` / `AdditiveAnimationTool.py` |

코드 adopt보다 **레이어 설계 참고**로 먼저 볼 것.

---

## ebadier/MotionBuilder-Tools

| 항목 | 내용 |
|------|------|
| URL | https://github.com/ebadier/MotionBuilder-Tools |
| 용도 | 씬 정리·애니 유틸 Python **모음** (스크립트별 독립) |
| 도입 | 쓸 `.py`만 [vendor/](scripts/vendor/README.md)에 복사 — repo 전체 submodule 비추 |

---

## SoerenFrohne/MotionBuilder-Pipeline-Scripts

| 항목 | 내용 |
|------|------|
| URL | https://github.com/SoerenFrohne/MotionBuilder-Pipeline-Scripts |
| 용도 | **다수 take·클립** 배치, 캐릭터 셋업 자동화 |
| 본인 파이프 | Retargeter(merge·retarget) **보조** — 세션·폴더 단위 파이프라인 참고 |

ML·실험 맥락: [ai-motion-cleanup.md](ai-motion-cleanup.md)

---

## alex3dbros/MotionbuilderPublicTools

| 항목 | 내용 |
|------|------|
| URL | https://github.com/alex3dbros/MotionbuilderPublicTools |
| 용도 | `Animation/` 모듈 등 Python 라이브러리 형태 |
| 설정 | 저장소 경로를 **환경 변수 PYTHONPATH** 또는 Mobu 스크립트 path에 추가 |

---

## awesome-motionbuilder

[matthewkapfhammer/awesome-motionbuilder](https://github.com/matthewkapfhammer/awesome-motionbuilder) — 포럼·튜토리얼·repo 큐레이션.  
사이트: https://matthewkapfhammer.github.io/awesome-motionbuilder/

### awesome에서 post용으로 고른 항목

**Git repo** (본 문서에 없거나 ★☆☆인 것 — 위 우선순위 표 참고)

| Repo | post와의 관계 |
|------|----------------|
| [eksod/additiveAnimation](https://github.com/eksod/additiveAnimation) | 레이어·additive — § eksod/additiveAnimation |
| [ebadier/MotionBuilder-Tools](https://github.com/ebadier/MotionBuilder-Tools) | § ebadier/MotionBuilder-Tools |
| [CountZer0/PipelineConstructionSet `/moBu`](https://github.com/CountZer0/PipelineConstructionSet/tree/master/python/moBu) | 스튜디오 파이프 **구조 참고** (전체 adopt X) |

**스킵** (awesome 목록에 있으나 본 파이프와 거리 있음)

| Repo | 이유 |
|------|------|
| [shotgunsoftware/tk-motionbuilder](https://github.com/shotgunsoftware/tk-motionbuilder) | Flow/ShotGrid TD |
| [ChaosGroup/vray-for-mobu](https://github.com/ChaosGroup/vray-for-mobu) | 렌더 |
| [pymobu (Google Code archive)](https://code.google.com/archive/p/pymobu/) | 아카이브 |

**글·튜토리얼** (repo 없이 읽기)

| 링크 | 주제 |
|------|------|
| [Vic DeBaie — Stop Foot Sliding](http://www.vicdebaie.com/blog/stop-foot-sliding-with-motionbuilder-and-python/) | 발 sliding + Python |
| [eksod.com — MotionBuilder](http://www.eksod.com/category/motionbuilder/) | Retargeter作者 |
| [Neill3d — scripts for MotionBuilder](http://neill3d.com/en/motionbuilder/scripts-for-motionbuilder) | OpenMoBu 맥락 |
| [Rigging Dojo — Mobu GDC tricks](http://www.riggingdojo.com/2016/08/30/animation-gdc-tricks-trade-motionbuilder/) | 리타겟 실무 팁 |
| [gameanim — seamless mocap cycles](http://www.gameanim.com/2013/09/11/seamless-mocap-cycles-tutorial/) | 루프 take |

---

## Cursor / VS Code 연동

### pyfbsdk 스텁 (편집·자동완성)

| 항목 | 내용 |
|------|------|
| PyPI | [`motionbuilder-stubs==2025.*`](https://pypi.org/project/motionbuilder-stubs/) |
| 생성기 (참고) | [nils-soderman/pyfbsdk-stub-generator](https://github.com/nils-soderman/pyfbsdk-stub-generator) → [Codeberg motionbuilder-stubs](https://codeberg.org/nils-soderman/motionbuilder-stubs) |
| 본 저장소 | `post/scripts/.venv` + [`.vscode/settings.json`](../.vscode/settings.json) |
| 설정 | [installation.md](installation.md#cursor--pylance-스텁-편집-전용) |

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
[배치] Retargeter                    → Phase 1~2 자동화
[브릿지] OpenMoBu ReCreateRig       → Retargeter 후 Phase 3 (CR plot)
[수동] retargeting-cleanup           → Phase 4~6 Control Rig · export
[보조] OpenMoBu StayOnFloor          → Phase 4.1 발
[레이어] layer-override · additiveAnimation 참고
[배치 참고] Pipeline-Scripts         → take·클립 폴더 운영
[개발] stubs + Utils                 → post/scripts/ 작성
[ML/AI] ai-motion-cleanup            → 실험
[허브] awesome-motionbuilder         → 추가 repo·튜토리얼 탐색
```

## TODO

- [x] Retargeter — `vendor/retargeter/` · Mobu `Scripts\Retargeter.py`
- [ ] OpenMoBu Release 2025 호환 테스트 · ReCreateRig / StayOnFloor 시험
- [ ] MotionBuilder Utils 확장 설치·Mobu attach 확인
- [ ] MotionScriptTools / ebadier — foot·씬 유틸 **1~2개**만 vendor 후 기록
