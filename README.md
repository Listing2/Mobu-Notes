# Mobu-Notes

모캡 스튜디오에서 쓰는 **MotionBuilder → Unity → 방송** 파이프라인 메모 저장소입니다.  
Mobu에서 어떻게 retarget·cleanup·export 하는지, 라이브 송출 때 무엇을 점검하는지를 **한곳에** 모아 둡니다.

| Stack | Version |
|-------|---------|
| MotionBuilder | **2025** |
| Unity | 타임라인·Cinemachine(post) / 실시간 수신(live) |

---

## post vs live — 뭐가 다른가

| | **post** | **live** |
|---|----------|----------|
| **언제** | 녹화된 **FBX**를 캐릭터에 맞출 때 | **방송·실시간** mocap 할 때 |
| **Mobu 역할** | Retarget · Control Rig cleanup · bake | 실시간 **stream** |
| **결과물** | cleanup FBX → Unity Animation | Unity 캐릭터 → OBS |
| **폴더** | [post/](post/) | [live/](live/) |

```text
post   mocap FBX → Mobu retarget → CR + Layer cleanup → skeleton plot → FBX → Unity
live   mocap → Mobu stream → Unity sync → OBS
shared 세션·버그 기록 템플릿
```

---

## Repository layout

```text
Mobu-Notes/
├── post/       FBX 후처리 (retarget, Control Rig, export)
├── live/       실시간 송출·방송·jitter checklist
├── shared/     issue log 템플릿
└── .vscode/    Python venv · motionbuilder-stubs
```

---

## Post pipeline (요약)

**매 take 작업할 때** → [실무 12단계](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)  
**처음 공부할 때** → [fundamentals](post/workflows/retargeting-fundamentals.md) → [cleanup](post/workflows/retargeting-cleanup.md) → [Unity import](post/unity-import.md)

| Step | Mobu에서 | 기억할 것 |
|------|----------|-----------|
| **Setup** | motion-only FBX · target characterize · Source · scale | Reference pose 확인 · **Plot 전 Hand IK 100 금지** |
| **Bake** | Plot to **Control Rig** · source 캐릭터 삭제 | full body + fingers · Key Reducer **Off** |
| **Fix** | **Animation Layer** + Weight · Foot IK | pose = layer · timing = **Weight** |
| **Export** | Plot to **Skeleton** · FBX | skeleton anim만 (CR·source 제외) |

손목·finger **drift**가 남으면 → [Layer 가이드](post/workflows/layer-override-hands-head.md) (Plot 전 Hand IK 100 / source 잔존 / Weight 없이 pose만 키)

---

## Doc map

### Post — learning path

1. [retargeting-fundamentals.md](post/workflows/retargeting-fundamentals.md) — Characterize, Match Source, plot이 **왜** 그런지
2. [retargeting-cleanup.md](post/workflows/retargeting-cleanup.md) — **실무 12단계** · Phase 0~6
3. [layer-override-hands-head.md](post/workflows/layer-override-hands-head.md) — hand · neck Layer + Weight
4. [unity-import.md](post/unity-import.md) — Unity FBX import

### Post — tools & scripts

| Doc | What |
|-----|------|
| [workflows/README.md](post/workflows/README.md) | workflow 목록 |
| [installation.md](post/installation.md) | Mobu path · Scripts · Cursor stub |
| [external-tools.md](post/external-tools.md) | Retargeter · OpenMoBu · refs |
| [scripts/README.md](post/scripts/README.md) | Python scripts index |
| [scripts/vendor/README.md](post/scripts/vendor/README.md) | vendor · Retargeter 실행법 |
| [ai-motion-cleanup.md](post/ai-motion-cleanup.md) | ML·실험 옵션 (정석은 Mobu CR) |

### Live

| Doc | What |
|-----|------|
| [live/README.md](live/README.md) | live hub |
| [live/pipeline/](live/pipeline/) | post + live overview |
| [live/motionbuilder/](live/motionbuilder/) | stream fps · Mobu live |
| [live/unity/](live/unity/) | live sync · ports |
| [live/troubleshooting/](live/troubleshooting/) | jitter · live issues |
| [live/checklists/](live/checklists/) | pre-broadcast checklist |

### Shared

| Doc | What |
|-----|------|
| [templates/issue-log.md](shared/templates/issue-log.md) | 세션·버그 기록 |

---

## External tools (in use)

| Tool | For | Warning |
|------|-----|---------|
| [Retargeter](https://github.com/eksod/Retargeter) | FBX folder batch retarget | **Python Editor** + vendor copy만. upstream을 `Scripts/`에 두면 **Mobu가 안 켜질 수 있음** |
| [OpenMoBu](https://github.com/Neill3d/OpenMoBu) | HIK · ReCreateRig · StayOnFloor | **Mobu 2025** build와 맞출 것 |
| [motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/) | Cursor autocomplete | [installation.md](post/installation.md) · `setup-dev.ps1` |

---

## Quick start

```powershell
# Cursor에서 Mobu Python 편집 (1회)
cd post/scripts
.\setup-dev.ps1
```

| I want to… | Open |
|------------|------|
| 오늘 take cleanup | [실무 12단계](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| Mobu path · Retargeter | [installation.md](post/installation.md) |
| 방송 전 점검 | [pre-broadcast checklist](live/checklists/pre-broadcast-mocap.md) |
| 버그·세션 기록 | [issue-log](shared/templates/issue-log.md) |

---

## Conventions

- 문서·주석·커밋: **한국어** (Mobu/Unity 용어는 English 그대로)
- 파일명·코드: **ASCII**
- 비밀·IP: `live/private/` 또는 placeholder
- 세션마다 기록: Mobu/Unity version, fps, take 출처, Match Source, plot reducer, export 옵션

---

## Links

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## License

MIT — [LICENSE](LICENSE).
