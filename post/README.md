# post — FBX Post-Process

모캡으로 **녹화한 FBX**를 MotionBuilder 2025에서 retarget·cleanup하고, Unity에 넣을 animation FBX로 export하는 작업입니다.

실시간 방송·stream 설정은 **[live/](../live/)** — 여기서 다루지 않습니다.

---

## Environment

| | |
|---|---|
| MotionBuilder | 2025 |
| Install path | [installation.md](installation.md) |
| Input | mocap FBX (motion-only 권장) |
| Output | cleanup FBX → [unity-import.md](unity-import.md) |

---

## Where to go

| Doc | When |
|-----|------|
| **[실무 12단계](workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)** | **오늘 take 작업** |
| [workflows/README.md](workflows/README.md) | 처음 읽을 때 · 문서 목록 |
| [retargeting-fundamentals.md](workflows/retargeting-fundamentals.md) | Match Source, plot 등 **개념** |
| [layer-override-hands-head.md](workflows/layer-override-hands-head.md) | hand · neck **Layer + Weight** |
| [installation.md](installation.md) | Mobu path · Scripts · Cursor stub |
| [external-tools.md](external-tools.md) | Retargeter · OpenMoBu |
| [ai-motion-cleanup.md](ai-motion-cleanup.md) | ML·실험 옵션 (참고) |
| [scripts/](scripts/) | Python · [vendor/](scripts/vendor/README.md) |
