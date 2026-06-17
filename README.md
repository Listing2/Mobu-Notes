# Mobu-Notes

<p align="center">
  <b>English</b> | <a href="./README.ko.md">한국어</a>
</p>

Studio notes for the **MotionBuilder -> Unity -> broadcast** mocap pipeline.
This repo keeps post-process, live-stream, scripts, and session templates in one place.

| Stack | Version |
|-------|---------|
| MotionBuilder | **2025** |
| Unity | Timeline/Cinemachine (post) / real-time receiver (live) |

---

## Post vs Live

| | **post** | **live** |
|---|----------|----------|
| **When** | Recorded **FBX** needs retarget/cleanup | Real-time mocap / broadcast |
| **Mobu role** | Retarget · Control Rig cleanup · bake | Real-time **stream** |
| **Output** | cleanup FBX -> Unity Animation | Unity character -> OBS |
| **Folder** | [post/](post/) | [live/](live/) |

```text
post   mocap FBX → Mobu retarget → CR + Layer cleanup → skeleton plot → FBX → Unity
live   mocap → Mobu stream → Unity sync → OBS
shared session / bug templates
```

---

## Repository layout

```text
Mobu-Notes/
├── post/       FBX post-process (retarget, Control Rig, export)
├── live/       real-time stream, broadcast, jitter checklist
├── shared/     issue-log templates
└── .vscode/    Python venv · motionbuilder-stubs
```

---

## Post Pipeline

**Daily take work** -> [practical flow](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)  
**First read** -> [fundamentals](post/workflows/retargeting-fundamentals.md) -> [cleanup](post/workflows/retargeting-cleanup.md) -> [Unity import](post/unity-import.md)

| Step | In Mobu | Watch |
|------|----------|-----------|
| **Setup** | motion-only FBX · Source QC · target characterize · scale | Fix source pops before Plot |
| **Bake** | Plot to **Control Rig** · remove source character | full body + fingers · Key Reducer **Off** |
| **Fix** | **Animation Layer** + Weight · Foot IK | hard finger hold may need Base finger flat |
| **Export** | Plot to **Skeleton** · FBX | skeleton animation only (exclude CR/source) |

For wrist/finger **drift** -> [Layer guide](post/workflows/layer-override-hands-head.md) (wrist IK · finger FK · Weight roles)

---

## Doc map

### Post — learning path

1. [retargeting-fundamentals.md](post/workflows/retargeting-fundamentals.md) — why Characterize, Match Source, and Plot matter
2. [retargeting-cleanup.md](post/workflows/retargeting-cleanup.md) — **practical flow** · Phase 0~6
3. [layer-override-hands-head.md](post/workflows/layer-override-hands-head.md) — hand · neck Layer + Weight
4. [unity-import.md](post/unity-import.md) — Unity FBX import

### Post — tools & scripts

| Doc | What |
|-----|------|
| [workflows/README.md](post/workflows/README.md) | workflow index |
| [installation.md](post/installation.md) | Mobu path · Scripts · Cursor stub |
| [external-tools.md](post/external-tools.md) | Retargeter · OpenMoBu · refs |
| [scripts/README.md](post/scripts/README.md) | Python scripts index |
| [scripts/vendor/README.md](post/scripts/vendor/README.md) | vendor · Retargeter usage |
| [ai-motion-cleanup.md](post/ai-motion-cleanup.md) | ML/experimental options (Mobu CR remains baseline) |

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
| [templates/issue-log.md](shared/templates/issue-log.md) | session / bug notes |

---

## External tools (in use)

| Tool | For | Warning |
|------|-----|---------|
| [Retargeter](https://github.com/eksod/Retargeter) | FBX folder batch retarget | Use **Python Editor** + vendor copy only. Upstream in `Scripts/` may prevent Mobu startup |
| [OpenMoBu](https://github.com/Neill3d/OpenMoBu) | HIK · ReCreateRig · StayOnFloor | Match the **Mobu 2025** build |
| [motionbuilder-stubs](https://pypi.org/project/motionbuilder-stubs/) | Cursor autocomplete | [installation.md](post/installation.md) · `setup-dev.ps1` |

---

## Quick start

```powershell
# One-time setup for editing Mobu Python in Cursor
cd post/scripts
.\setup-dev.ps1
```

| I want to… | Open |
|------------|------|
| Clean today's take | [practical flow](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| Mobu path · Retargeter | [installation.md](post/installation.md) |
| Pre-broadcast checks | [pre-broadcast checklist](live/checklists/pre-broadcast-mocap.md) |
| Session / bug note | [issue-log](shared/templates/issue-log.md) |

---

## Conventions

- Main README files: **English first**. Korean notes are OK where useful.
- File names and code: **ASCII**
- Keep secrets/IPs in `live/private/` or use placeholders.
- Log each session: Mobu/Unity version, fps, take source, Match Source, plot reducer, export options.

---

## Links

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## License

MIT — [LICENSE](LICENSE).
