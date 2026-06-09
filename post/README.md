# post — FBX 후처리

모션캡처 **녹화 FBX**를 MotionBuilder 2025에서 리타게팅·클린업하고 export하는 작업.

라이브 송출·방송은 **[live/](../live/)** 와 분리.

## 환경

| 항목 | 값 |
|------|-----|
| MotionBuilder | 2025 |
| InstallPath (로컬) | [installation.md](installation.md) |
| 입력 | 모캡 등으로 녹화한 FBX |
| 출력 | 클린업 FBX → [unity-import.md](unity-import.md) |

## 문서

| 경로 | 내용 |
|------|------|
| [workflows/](workflows/) | 리타게팅·클린업 절차 (**읽는 순서** 포함) |
| [installation.md](installation.md) | Mobu 경로 · Cursor 스텁 · Scripts 연결 |
| [scripts/](scripts/) | Python · [vendor/](scripts/vendor/README.md) |
| [external-tools.md](external-tools.md) | Retargeter, OpenMoBu 등 |
| [ai-motion-cleanup.md](ai-motion-cleanup.md) | AI · ML 클린업 옵션 |

## 한 줄 요약

Characterize → Retarget(Match Source Off) → Control Rig 클린업 → Skeleton plot → FBX export
