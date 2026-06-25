# Scripts — Mobu Python

MotionBuilder 2025 `pyfbsdk` automation and batch scripts. **Run inside Mobu**; the Cursor venv is only for editing/autocomplete.

Tool code and short UI labels use English; longer in-Mobu guidance can use Korean for quick visual checks.

---

## Inventory

| Path | What | Run |
|------|------|-----|
| [noise_cleaner.py](noise_cleaner.py) | Selected Source/CR FCurve smoothing tool | Python Editor · Tool window |
| [finger_preset_tool.py](finger_preset_tool.py) | Finger FK pose capture / apply / hold | Python Editor · Tool window |
| [pose_blend_tool.py](pose_blend_tool.py) | Blend selected arm/upper-body controls toward a target pose | Python Editor · Tool window |
| [startup/mobu_notes_menu.py](startup/mobu_notes_menu.py) | Adds the top-level `Mobu Notes` menu | copy/link to user `PythonStartup` |
| [vendor/retargeter/retargeter.py](vendor/retargeter/retargeter.py) | [Retargeter](https://github.com/eksod/Retargeter) — FBX batch retarget | Python Editor · **vendor copy only** |
| [vendor/](vendor/README.md) | external GitHub repos | see vendor guide |

Tool catalog: [external-tools.md](../external-tools.md)

---

## Run in Mobu

| Method | |
|--------|---|
| Python Editor | `Window` -> `Python Editor` -> Open -> Execute |
| Scripts menu | `bin\config\Scripts\` — [installation.md](../installation.md) |
| Cursor Utils | [MotionBuilder Utils](../external-tools.md#motionbuilder-utils-실행디버그) — Ctrl+Enter |

Path · stub · `setup-dev.ps1`: **[installation.md](../installation.md)** (single source)

---

## Conventions

- File names / identifiers: ASCII
- Script header: Mobu version and run method

## Cleanup Tools Quick Use

### Noise cleaner

1. Open / Execute `noise_cleaner.py` in Python Editor.
2. In **Mobu Noise Cleaner**, set frame range, strength, radius, and passes.
3. Select one or many Source bones / CR controls.
4. Run `Clean Rotation`, `Clean Translation`, or `Clean All`.
5. Use `Flatten` for a hard A-B value hold; use `Hold Keys` for a blended hold.
6. Check tool status and play the result.

Use Source cleanup before retarget by selecting the Source skeleton. Use CR cleanup after Plot to CR by selecting CR controls.
`Clean` reduces jitter with neighbor-key averaging. `Spike` finds/fixes short pops. `Flatten` holds the start-frame value through the end frame.

### Mobu Notes menu

`.py` files in `Scripts` may not always show up in `Python Tools`. The most reliable setup is to copy `startup/mobu_notes_menu.py` into the user config `PythonStartup` folder so Mobu creates a top-level `Mobu Notes` menu.

```powershell
$MobuStartup = "C:\Users\user\MB\2025\config\PythonStartup"
Copy-Item .\startup\mobu_notes_menu.py $MobuStartup
```

Restart Mobu. A top-level `Mobu Notes` menu should appear with `Noise Cleaner`, `Finger Preset Tool`, and `Pose Blend Tool`.

### Finger preset

1. Run `finger_preset_tool.py`.
2. Multi-select the Finger FK controls (Ctrl+click in viewer/Navigator). One Capture/Apply/Zero acts on the whole selection.
3. Pose fist / open / index-point / grip, then `Capture A/B/C` (session-only) or type a name and `Save / Overwrite` (persistent preset).
4. With the same selection, use `Apply` / `Apply Preset`, or set a frame range and `Hold` / `Hold Preset`.
5. Use `Zero Current`, `Zero Range`, or `Zero All Keys` to reset selected rotation curves to `0`.

Presets are stored by control name (`model` + rotation path), so selection order no longer has to match. Named presets persist to `~/.mobu_notes/finger_presets.json`; `List Presets` shows saved names, `Delete Preset` removes one. A/B/C remain fast session-only slots.

For dance/group choreography, repeated pose presets + range hold + light noise clean are usually faster than editing every finger detail.

### Pose blend

1. Run `pose_blend_tool.py`.
2. Key the desired arm / upper-body pose on the Target frame.
3. Select arm, wrist, shoulder, chest, neck/head controls.
4. Set Start / Target / End / Strength, then run `Blend To Target`.

Controls whose names include root / hips / leg / foot / toe / ankle are ignored. Use this for matching a pose on a dance beat while preserving surrounding motion.

## MotionBuilder Filters

| Filter | Use | Watch |
|--------|------|------|
| Butterworth | low-pass smoothing for mocap jitter | too low cutoff kills motion feel |
| Key Reducing | reduce unnecessary keys | can cause sliding on foot/hand contact |
| Constant Key Reducer | remove repeated constant keys | use conservatively before export |
| Gimbal Killer / Unroll | reduce rotation flips | use after checking the cause |

Repo tools are not replacements for Filters; they are quick practical buttons for selected controls/ranges.

## Template

```python
# Mobu 2025 - one-line description
# Run: Window -> Python Editor -> Execute

from pyfbsdk import *  # noqa: F403

def main() -> None:
    pass

if __name__ in ("__main__", "__builtin__"):
    main()
```

---

## Links

- [installation.md](../installation.md) · [vendor/README.md](vendor/README.md)
- [retargeting-cleanup.md](../workflows/retargeting-cleanup.md)
