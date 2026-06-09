# MotionBuilder 실무 (Mobu 2025)

모션캡처 FBX를 MotionBuilder에서 **리타게팅·클린업**하고 Unity(시네머신 등)로 가져가는 작업을 정리합니다.

`docs/`는 송출·파이프라인·트러블슈팅 등 **운영 노트**, `mobu/`는 **FBX 애니메이션·캐릭터 작업**을 다룹니다.

## 환경

| 항목 | 값 |
|------|-----|
| MotionBuilder | 2025 |
| 입력 | 모캡 등으로 녹화한 FBX |
| 캐릭터 | VRM 또는 FBX → FBX export 후 Mobu characterize |
| 출력 | 클린업된 FBX → Unity import |

## 문서 — 읽는 순서

| 순서 | 문서 | 내용 |
|------|------|------|
| 1 | [workflows/retargeting-fundamentals.md](workflows/retargeting-fundamentals.md) | 알아야 할 개념·옵션·실수 |
| 2 | [workflows/retargeting-cleanup.md](workflows/retargeting-cleanup.md) | Phase 0~6 실무 절차 |
| 3 | [docs/unity/animation-import-fbx.md](../docs/unity/animation-import-fbx.md) | Unity FBX import |

| 경로 | 내용 |
|------|------|
| [workflows/README.md](workflows/README.md) | 워크플로 목록 |
| [scripts/README.md](scripts/README.md) | Mobu Python 스크립트 (추가 예정) |

## 핵심만 (한 줄)

Characterize(소스·타겟) → pose·스케일 → Retarget(Match Source Off) → Control Rig 클린업 → Skeleton plot → FBX export

## 빠른 링크

- [개념 정리](workflows/retargeting-fundamentals.md)
- [실무 절차](workflows/retargeting-cleanup.md)
- Match Source **Off**, 스케일을 모션 스케일에 맞추기
- Foot sliding — Mobu Control Rig 1차, Unity compression 2차
