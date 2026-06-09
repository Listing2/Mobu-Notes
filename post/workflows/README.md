# 워크플로

MotionBuilder **후처리(post)** — 캐릭터·모션 FBX 절차. 라이브 송출: [live/](../../live/).

## 목록

| 문서 | 설명 |
|------|------|
| [retargeting-fundamentals.md](retargeting-fundamentals.md) | **개념·옵션·원인** — Characterize, pose, mapping, plot, export |
| [retargeting-cleanup.md](retargeting-cleanup.md) | **실무 절차** — Phase 0~6 + [Animation Layer 파이프](retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| [layer-override-hands-head.md](layer-override-hands-head.md) | **손·Neck/Head** Animation Layer + Weight |
| (작성 예정) `character-setup.md` | VRM/FBX → Mobu characterize, 씬 템플릿 |
| (작성 예정) `export-presets.md` | FBX export 프리셋·네이밍 |

## 외부 도구

- [external-tools.md](../external-tools.md) — 도구 카탈로그
- [ai-motion-cleanup.md](../ai-motion-cleanup.md) — AI · ML 클린업
- [installation.md](../installation.md) · [scripts/vendor/](../scripts/vendor/README.md) — Mobu 경로 · GitHub 코드 추가

## 읽는 순서 (추천)

1. [retargeting-fundamentals.md](retargeting-fundamentals.md) — 왜 그렇게 하는지
2. [retargeting-cleanup.md](retargeting-cleanup.md) — 실제 작업 순서
3. [unity-import.md](../unity-import.md) — Unity import

## 기록할 때 포함할 항목

- MotionBuilder 버전 (2025)
- 소스 모션 출처 (모캡 프로그램, 파일명, fps)
- 타겟 캐릭터 (리그 타입, export 툴)
- Retarget (Match Source, 스케일)
- Plot 옵션 (reducer, root translation)
- Export / Unity import 설정
