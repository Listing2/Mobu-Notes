# AI · 코딩 기반 모션 클린업

Mobu **Control Rig 수작업** 외에, 스크립트·딥러닝·다른 DCC로 클린업을 보조하는 옵션 요약.  
본 저장소 파이프의 **정석은 여전히** [retargeting-cleanup.md](workflows/retargeting-cleanup.md) (Phase 4 Control Rig).

---

## 한 줄 정리

| 방식 | 성숙도 | 본인 파이프와의 관계 |
|------|--------|----------------------|
| **Mobu Python** (규칙·FCurve·IK) | 실무 표준 | **지금 바로** — [external-tools.md](external-tools.md) |
| **딥러닝** (접지·footskate·노이즈) | 연구·실험 | FBX↔중간 포맷 브릿지 필요 |
| **AI 마커리스 캡처** | 상용 확산 | 캡처는 쉬워지고 **클린업 부담은 downstream**으로 이동 |

AI mocap 도입 시에도 “캡처만 AI, **가공은 Mobu post**” 구조가 흔하다.

---

## 1. Mobu + Python (코딩 클린업)

AI가 아니지만 **가장 많이 쓰는 자동화**. Control Rig bake **전·후** 보조.

- **도구 목록:** [external-tools.md](external-tools.md) (Retargeter, MotionScriptTools, 발 스크립트 등)
- **repo 추가·실행:** [scripts/vendor/README.md](scripts/vendor/README.md)
- **Mobu 경로·스텁:** [installation.md](installation.md)

추가 참고 (카탈로그 미포함):

| 리소스 | 링크 | 용도 |
|--------|------|------|
| Stop Foot Sliding | [Vic DeBaie](http://www.vicdebaie.com/blog/stop-foot-sliding-with-motionbuilder-and-python/) | 레이어·참조 프레임 |
| mocap 파이프라인 | [MotionBuilder-Pipeline-Scripts](https://github.com/SoerenFrohne/MotionBuilder-Pipeline-Scripts) | 클립 배치·캐릭터 셋업 |

---

## 2. 딥러닝 · 연구 (foot skate · 노이즈 · 리타겟)

Mobu에 **직접 플러그인** 형태로 붙는 경우는 드물다. 보통 **Python 파이프 → 결과를 FBX/BVH로 다시 import**.

### 발 sliding · 접지

| 프로젝트 | 링크 | 요약 |
|----------|------|------|
| **UnderPressure** | [InterDigitalInc/UnderPressure](https://github.com/InterDigitalInc/UnderPressure) | vGRF 추정 → 접지 검출 → **footskate IK 클린업** (`demo.py`) |
| **StableMotion** | [arXiv 2505.03154](https://arxiv.org/html/2505.03154v1) | 깨진 mocap을 **unpaired**로 학습 — foot skate, frozen frame 등 |
| **StableMoFusion** | [Linketic/StableMoFusion](https://github.com/h-y1heng/StableMoFusion) | UnderPressure 연동, `--footskate_cleanup` |

### 캡처 원본 노이즈 (볼륨·마커)

| 프로젝트 | 링크 | 요약 |
|----------|------|------|
| **MoCap-Solver** | [NetEase-GameAI/MoCap-Solver](https://github.com/NetEase-GameAI/MoCap-Solver) | 마커 노이즈 → 클린 스켈레톤 (SIGGRAPH 2021) |
| **FootNet** | [adrianrivadulla/FootNet](https://github.com/adrianrivadulla/FootNet) | 관절 궤적으로 heel strike / toe off 검출 |

### AI 리타겟 (로봇·연구 비중)

| 프로젝트 | 링크 | 비고 |
|----------|------|------|
| GMR | [YanjieZe/GMR](https://github.com/YanjieZe/GMR) | FBX 등 → 휴머노이드 **로봇**, 실시간 |
| MeshRet | [XRerate/MeshRet](https://github.com/XRerate/MeshRet) | 접지·penetration 의식 스킨 리타겟 |
| IKMR | [Cybercal/IKMR](https://github.com/Cybercal/IKMR) | 신경망 human→humanoid |

게임/VTuber 캐릭터 FBX 후처리와는 **데이터 형식·목적**이 다를 수 있음.

---

## 3. AI 캡처 · 다른 DCC

캡처 단계가 AI/마커리스여도 **클린업 단계는 남는다**.

| 유형 | 예 | 클린업 쪽 |
|------|-----|-----------|
| AI 마커리스 | Move.ai, RADiCAL, DeepMotion 등 | 발·관절 아티팩트 → Mobu 또는 엔진 |
| 물리 보정 DCC | [Cascadeur](https://cascadeur.com/) | mocap unbake → auto-physics → 수동 polish |
| 엔진 내 | Unity / Unreal Control Rig, IK Retargeter | [unity-import.md](unity-import.md), live 쪽 |

참고 글: [AI mocap과 파이프라인 (Keuru)](https://kevurugames.com/blog/ai-motion-capture-and-the-future-of-3d-animation-companies/) — 캡처 비용↓, **cleanup·retarget 부담↑**

---

## 4. 본인 post 파이프에 붙일 때

```text
[현재 정석]
  FBX → Mobu Retarget → Control Rig 수동 → Skeleton bake → export

[코딩 1단계]  Retargeter + foot sliding Python
[ML 실험]     UnderPressure 등 — SMPL/BVH 브릿지 후 Mobu merge
[아직 멀]     Control Rig 디테일까지 AI 완전 대체
```

| ML/AI가 잘 맞는 경우 | Mobu 수작업이 나은 경우 |
|----------------------|-------------------------|
| take 많고 동작 패턴 반복 | VRM/게임 캐 비율·손·연출 디테일 |
| foot skate·접지가 주 증상 | take마다 스케일·체형 다름 |
| 마커 노이즈 심한 볼륨 원본 | 시네마·타임라인용 의도적 수정 |

---

## 5. 우선 탐색 순서

1. [external-tools.md](external-tools.md) + [vendor/README.md](scripts/vendor/README.md) — Mobu Python·배치 retarget
2. [UnderPressure](https://github.com/InterDigitalInc/UnderPressure) — foot skate ML (`demo.py`)
3. [StableMotion 논문](https://arxiv.org/html/2505.03154v1) — unpaired cleanup 방향

---

## 관련

- [external-tools.md](external-tools.md) — Mobu Python·Retargeter·OpenMoBu
- [retargeting-fundamentals.md](workflows/retargeting-fundamentals.md) §10 Foot Sliding
- [retargeting-cleanup.md](workflows/retargeting-cleanup.md) — Phase 4 Control Rig
