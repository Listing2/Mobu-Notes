# Scripts — Mobu Python

Mobu 2025 `pyfbsdk` 자동화·배치 스크립트. **실행은 Mobu 내부** — Cursor venv는 편집·autocomplete 전용.

---

## Inventory

| Path | What | Run |
|------|------|-----|
| [noise_cleaner.py](noise_cleaner.py) | 선택한 Source/CR FCurve 구간 smoothing tool | Python Editor · Tool 창 |
| [finger_preset_tool.py](finger_preset_tool.py) | Finger FK pose capture / apply / hold | Python Editor · Tool 창 |
| [pose_blend_tool.py](pose_blend_tool.py) | 선택한 팔·상체 컨트롤을 target pose로 부드럽게 유도 | Python Editor · Tool 창 |
| [startup/mobu_notes_menu.py](startup/mobu_notes_menu.py) | 상단 `Mobu Notes` 메뉴 자동 추가 | user config `PythonStartup`에 복사/링크 |
| [launchers/mobu_notes_tools_launcher.py](launchers/mobu_notes_tools_launcher.py) | 수동 실행용 허브 런처 | user config `Scripts`에 복사/링크 |
| [vendor/retargeter/retargeter.py](vendor/retargeter/retargeter.py) | [Retargeter](https://github.com/eksod/Retargeter) — FBX batch retarget | Python Editor · **vendor copy only** |
| [vendor/](vendor/README.md) | external GitHub repos | see vendor guide |

Tool catalog: [external-tools.md](../external-tools.md)

---

## Run in Mobu

| Method | |
|--------|---|
| Python Editor | `Window` → `Python Editor` → Open → Execute |
| Scripts menu | `bin\config\Scripts\` — [installation.md](../installation.md) |
| Cursor Utils | [MotionBuilder Utils](../external-tools.md#motionbuilder-utils-실행디버그) — Ctrl+Enter |

Path · stub · `setup-dev.ps1`: **[installation.md](../installation.md)** (single source)

---

## Conventions

- 파일명·식별자: ASCII · 주석: 한국어
- 스크립트 상단: Mobu version · 실행 방법

## Cleanup tools quick use

### Noise cleaner

1. `noise_cleaner.py`를 Python Editor에서 Open / Execute.
2. **Mobu Noise Cleaner** Tool 창이 뜨면 frame range, strength, radius, passes 입력.
3. Source bone 또는 CR control 선택. 손가락처럼 여러 본/컨트롤을 동시에 선택해도 됨.
4. `Clean Rotation`, `Clean Translation`, `Clean All` 중 하나 실행.
5. A~B 구간을 한 값으로 고정하려면 `Flatten`, 자연스럽게 hold 키를 만들려면 `Hold Keys` 실행.
6. Tool 창 status와 Play 결과 확인.

Source cleanup은 retarget 전 Source skeleton을 선택해서 실행. CR cleanup은 Plot to CR 이후 소스 제거 후 CR 컨트롤을 선택해서 실행.
`Clean`은 주변 키 평균으로 jitter를 줄이고, `Spike`는 한두 프레임 pop을 찾거나 고친다. `Flatten`은 start frame 값을 end frame까지 유지한다.

### Menu / launcher

`Scripts` 폴더의 `.py`는 버전/설정에 따라 `Python Tools` 메뉴에 자동으로 안 보일 수 있다. 가장 확실한 방식은 `startup/mobu_notes_menu.py`를 user config `PythonStartup` 폴더에 복사해서 상단 `Mobu Notes` 메뉴를 직접 추가하는 것이다.

```powershell
$MobuStartup = "C:\Users\user\MB\2025\config\PythonStartup"
Copy-Item .\startup\mobu_notes_menu.py $MobuStartup
```

Mobu 재시작 후 상단 메뉴에 `Mobu Notes`가 생기고, 그 안에서 `Noise Cleaner`, `Finger Preset Tool`, `Pose Blend Tool`을 실행한다.

수동 허브 런처가 필요하면 `launchers/mobu_notes_tools_launcher.py`를 `Scripts` 폴더에 복사해서 Python Tool Manager / Python Tools 쪽에서 직접 등록한다.

### Finger preset

1. `finger_preset_tool.py` 실행.
2. Finger FK 15개 컨트롤을 같은 순서로 선택.
3. 주먹 / 펼침 / 검지 pose를 만든 뒤 `Capture A/B/C`.
4. 같은 선택 상태에서 `Apply` 또는 frame range 입력 후 `Hold`.

댄스·군무는 개별 손가락 디테일보다 **반복 pose preset + 구간 hold + 약한 noise clean** 조합이 빠르다.

### Pose blend

1. `pose_blend_tool.py` 실행.
2. Target frame에서 원하는 팔·상체 pose 키를 찍음.
3. 팔, 손목, 어깨, chest, neck/head 등 컨트롤 선택.
4. Start / Target / End / Strength 설정 후 `Blend To Target`.

Root / hips / leg / foot / toe / ankle 이름이 들어간 컨트롤은 자동 제외한다. 댄스·군무에서 특정 박자 포즈만 맞추고 앞뒤 motion은 살릴 때 사용.

## MotionBuilder Filters 메모

| Filter | 용도 | 주의 |
|--------|------|------|
| Butterworth | mocap jitter용 low-pass smoothing | 너무 낮은 cutoff는 동작 맛이 죽음 |
| Key Reducing | 불필요한 키 수 줄이기 | 발/손 contact에 쓰면 sliding 가능 |
| Constant Key Reducer | 같은 값 반복 키 정리 | export 전 보수적으로 |
| Gimbal Killer / Unroll | 회전 flip 완화 | 원인 확인 후 사용 |

본 저장소 툴은 Filters 대체가 아니라 **선택 본/구간에 빠르게 적용하는 실무 버튼** 용도.

## Template

```python
# Mobu 2025 — 설명 한 줄
# 실행: Window → Python Editor → Execute

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
