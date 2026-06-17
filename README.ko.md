# Mobu-Notes

<p align="center">
  <a href="./README.md">English</a> | <b>한국어</b>
</p>

모캡 스튜디오에서 쓰는 **MotionBuilder -> Unity -> 방송** 파이프라인 메모 저장소입니다.
녹화 FBX 후처리, 라이브 스트림, 스크립트, 세션 기록 템플릿을 한곳에 모아 둡니다.

| Stack | Version |
|-------|---------|
| MotionBuilder | **2025** |
| Unity | Timeline/Cinemachine (post) / 실시간 수신 (live) |

---

## Post vs Live

| | **post** | **live** |
|---|----------|----------|
| **언제** | 녹화된 **FBX**를 retarget/cleanup할 때 | 실시간 mocap / 방송 |
| **Mobu 역할** | Retarget · Control Rig cleanup · bake | real-time **stream** |
| **결과물** | cleanup FBX -> Unity Animation | Unity character -> OBS |
| **폴더** | [post/](post/) | [live/](live/) |

```text
post   mocap FBX -> Mobu retarget -> CR + Layer cleanup -> skeleton plot -> FBX -> Unity
live   mocap -> Mobu stream -> Unity sync -> OBS
shared session / bug 기록 템플릿
```

---

## Repository Layout

```text
Mobu-Notes/
├── post/       FBX 후처리 (retarget, Control Rig, export)
├── live/       실시간 stream, 방송, jitter checklist
├── shared/     issue-log templates
└── .vscode/    Python venv · motionbuilder-stubs
```

---

## Post Pipeline

**매 take 작업할 때** -> [실무 순서](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)  
**처음 읽을 때** -> [fundamentals](post/workflows/retargeting-fundamentals.md) -> [cleanup](post/workflows/retargeting-cleanup.md) -> [Unity import](post/unity-import.md)

| Step | Mobu에서 | 기억할 것 |
|------|----------|-----------|
| **Setup** | motion-only FBX · Source QC · target characterize · scale | 원본 pop은 Plot 전 source에서 먼저 정리 |
| **Bake** | Plot to **Control Rig** · source character 제거 | full body + fingers · Key Reducer **Off** |
| **Fix** | **Animation Layer** + Weight · Foot IK | hard finger hold는 Base finger flat 옵션 |
| **Export** | Plot to **Skeleton** · FBX | skeleton animation만 export (CR/source 제외) |

wrist/finger **drift**가 남으면 -> [Layer guide](post/workflows/layer-override-hands-head.md) (wrist IK · finger FK · Weight 역할 분리)

---

## Doc Map

### Post — Learning Path

1. [retargeting-fundamentals.md](post/workflows/retargeting-fundamentals.md) — Characterize, Match Source, Plot이 왜 중요한지
2. [retargeting-cleanup.md](post/workflows/retargeting-cleanup.md) — **실무 순서** · Phase 0~6
3. [layer-override-hands-head.md](post/workflows/layer-override-hands-head.md) — hand · neck Layer + Weight
4. [unity-import.md](post/unity-import.md) — Unity FBX import

### Post — Tools & Scripts

| Doc | What |
|-----|------|
| [workflows/README.md](post/workflows/README.md) | workflow index |
| [installation.md](post/installation.md) | Mobu path · Scripts · Cursor stub |
| [external-tools.md](post/external-tools.md) | Retargeter · OpenMoBu · refs |
| [scripts/README.md](post/scripts/README.md) | Python scripts index |
| [scripts/vendor/README.md](post/scripts/vendor/README.md) | vendor · Retargeter usage |
| [ai-motion-cleanup.md](post/ai-motion-cleanup.md) | ML/experimental options (기본은 Mobu CR) |

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
| [templates/issue-log.md](shared/templates/issue-log.md) | session / bug 기록 |

---

## External Tools

| Tool | For | Warning |
|------|-----|---------|
| [Retargeter](https://github.com/eksod/Retargeter) | FBX folder batch retarget | **Python Editor** + vendor copy만 사용. upstream 원본을 `Scripts/`에 넣으면 Mobu가 안 켜질 수 있음 |
| [OpenMoBu](https://github.com/Neill3d/OpenMoBu) | HIK · ReCreateRig · StayOnFloor | **Mobu 2025** build와 맞출 것 |
| [motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/) | Cursor autocomplete | [installation.md](post/installation.md) · `setup-dev.ps1` |

---

## Quick Start

```powershell
# Cursor에서 Mobu Python 편집용 1회 설정
cd post/scripts
.\setup-dev.ps1
```

| I want to... | Open |
|--------------|------|
| 오늘 take cleanup | [실무 순서](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| Mobu path · Retargeter | [installation.md](post/installation.md) |
| 방송 전 점검 | [pre-broadcast checklist](live/checklists/pre-broadcast-mocap.md) |
| 세션·버그 기록 | [issue-log](shared/templates/issue-log.md) |

---

## Conventions

- Main README files: **English first**, with this Korean version linked from the top.
- File names and code: **ASCII**
- Secrets/IPs: keep under `live/private/` or use placeholders.
- Log every session: Mobu/Unity version, fps, take source, Match Source, plot reducer, export options.

---

## Links

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## License

MIT — [LICENSE](LICENSE).
