# post — FBX 후처리

모션캡처 **녹화 FBX**를 MotionBuilder 2025에서 리타게팅·클린업하고 export하는 작업.

라이브 송출·방송 설정은 **[live/](../live/)** 와 분리.

## 환경

| 항목 | 값 |
|------|-----|
| MotionBuilder | 2025 |
| InstallPath (로컬) | `E:\AutoDesk\MotionBuilder\MotionBuilder 2025\` — [installation.md](installation.md) |
| 입력 | 모캡 등으로 녹화한 FBX |
| 출력 | 클린업된 FBX → Unity import — [unity-import.md](unity-import.md) |

## 읽는 순서

| # | 문서 |
|---|------|
| 1 | [workflows/retargeting-fundamentals.md](workflows/retargeting-fundamentals.md) |
| 2 | [workflows/retargeting-cleanup.md](workflows/retargeting-cleanup.md) |
| 3 | [unity-import.md](unity-import.md) |

| 경로 | 내용 |
|------|------|
| [workflows/](workflows/) | 워크플로 |
| [scripts/](scripts/) | Python · Cursor 스텁 |
| [installation.md](installation.md) | Mobu 폴더 경로 |
| [external-tools.md](external-tools.md) | Retargeter, OpenMoBu 등 |
| [ai-motion-cleanup.md](ai-motion-cleanup.md) | AI · ML · 코딩 클린업 옵션 |

## Python / Cursor

```powershell
cd post/scripts
.\setup-dev.ps1
```

## 한 줄 요약

Characterize → Retarget(Match Source Off) → Control Rig 클린업 → Skeleton plot → FBX export
