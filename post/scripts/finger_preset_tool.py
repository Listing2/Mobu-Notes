# Mobu 2025 - finger FK pose preset tool
# Run: Window -> Python Editor -> Open -> Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403
import json
import os
import traceback


START_FRAME = 0
END_FRAME = 30
BLEND_FRAMES = 2

_TOOL_NAME = "손가락 포즈 프리셋"
_TOOL_REF = None
_SLOTS = {
    "A": [],
    "B": [],
    "C": [],
}
_PRESETS = {}  # name -> [{"model", "path", "value"}]


def _preset_file_path():  # 프리셋 영구 저장 위치 (사용자 홈)
    return os.path.join(os.path.expanduser("~"), ".mobu_notes", "finger_presets.json")


def _frame_time(frame):
    return FBTime(0, 0, 0, int(frame))


def _selected_models():
    models = FBModelList()
    FBGetSelectedModels(models)
    return list(models)


def _current_time():
    try:
        return FBSystem().LocalTime
    except Exception:
        return FBPlayerControl().GetEditCurrentTime()


def _iter_animation_nodes(node, path=""):
    if node is None:
        return

    name = getattr(node, "Name", "") or ""
    next_path = (path + "/" + name).lower()

    yield node, next_path

    for child in node.Nodes:
        for item in _iter_animation_nodes(child, next_path):
            yield item


def _rotation_nodes_for_selection():
    items = []
    for model in _selected_models():
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not ("rotation" in path or "rotate" in path):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            items.append((model.Name, path, fcurve))

    return items


def _rotation_nodes_for_zeroing():
    items = []
    for model in _selected_models():
        try:
            model.Rotation.SetAnimated(True)
            root_node = model.Rotation.GetAnimationNode()
        except Exception:
            root_node = None

        for node, path in _iter_animation_nodes(root_node, "rotation"):
            fcurve = node.FCurve
            if fcurve is None:
                continue

            items.append((model.Name, path, fcurve))

    return items


def _key_indices_in_range(fcurve, start_time, end_time):
    start_ticks = start_time.Get()
    end_ticks = end_time.Get()
    indices = []

    for index, key in enumerate(fcurve.Keys):
        tick = key.Time.Get()
        if start_ticks <= tick <= end_ticks:
            indices.append(index)

    return indices


def _capture_entries():  # 현재 선택된 rotation 커브의 현재 프레임 값 수집
    time = _current_time()
    entries = []
    for model_name, path, fcurve in _rotation_nodes_for_selection():
        entries.append({
            "model": model_name,
            "path": path,
            "value": float(fcurve.Evaluate(time)),
        })
    return entries


def _match_entries(entries):  # 저장값을 현재 선택 커브에 이름(model+path) 기준으로 매칭
    items = _rotation_nodes_for_selection()
    lookup = {(model_name, path): fcurve for model_name, path, fcurve in items}

    matches = []
    for entry in entries:
        fcurve = lookup.get((entry.get("model"), entry.get("path")))
        if fcurve is not None:
            matches.append((fcurve, entry["value"]))

    if not matches and entries and items:  # 이름 매칭 0개면 선택 순서(index)로 폴백
        count = min(len(entries), len(items))
        matches = [(items[index][2], entries[index]["value"]) for index in range(count)]

    return matches, len(entries), len(items)


def _apply_entries(entries, label):
    matches, preset_count, selected_count = _match_entries(entries)
    if not matches:
        return "{0}: empty or no matching selection.".format(label)

    time = _current_time()
    key_count = 0
    for fcurve, value in matches:
        fcurve.KeyAdd(time, value)
        key_count += 1

    FBSystem().Scene.Evaluate()
    return (
        "Applied {label}\n"
        "Stored curves: {preset}\n"
        "Selected curves: {selected}\n"
        "Keyed curves: {keys}"
    ).format(
        label=label,
        preset=preset_count,
        selected=selected_count,
        keys=key_count,
    )


def _hold_entries(entries, start_frame, end_frame, blend_frames, label):
    matches, preset_count, selected_count = _match_entries(entries)
    if not matches:
        return "{0}: empty or no matching selection.".format(label)

    first_frame = int(min(start_frame, end_frame))
    last_frame = int(max(start_frame, end_frame))
    blend_frames = max(0, int(blend_frames))

    pre_time = _frame_time(first_frame - blend_frames)
    start_time = _frame_time(first_frame)
    end_time = _frame_time(last_frame)
    post_time = _frame_time(last_frame + blend_frames)

    key_count = 0
    for fcurve, value in matches:
        pre_value = float(fcurve.Evaluate(pre_time))
        post_value = float(fcurve.Evaluate(post_time))
        fcurve.KeyAdd(pre_time, pre_value)
        fcurve.KeyAdd(start_time, value)
        fcurve.KeyAdd(end_time, value)
        fcurve.KeyAdd(post_time, post_value)
        key_count += 4

    FBSystem().Scene.Evaluate()
    return (
        "Hold {label}\n"
        "Frame range: {start} - {end}\n"
        "Blend frames: {blend}\n"
        "Stored curves: {preset}\n"
        "Selected curves: {selected}\n"
        "Added keys: {keys}"
    ).format(
        label=label,
        start=first_frame,
        end=last_frame,
        blend=blend_frames,
        preset=preset_count,
        selected=selected_count,
        keys=key_count,
    )


def capture_slot(slot_name):
    entries = _capture_entries()
    if not entries:
        return "No selected finger FK rotation curves."

    _SLOTS[slot_name] = entries
    return "Captured slot {0}\nRotation curves: {1}".format(slot_name, len(entries))


def apply_slot(slot_name):
    return _apply_entries(_SLOTS.get(slot_name, []), "slot " + slot_name)


def hold_slot(slot_name, start_frame, end_frame, blend_frames):
    return _hold_entries(_SLOTS.get(slot_name, []), start_frame, end_frame, blend_frames, "slot " + slot_name)


def load_presets():  # 시작 시 JSON에서 프리셋 로드
    global _PRESETS
    path = _preset_file_path()
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                _PRESETS = data
    except Exception:
        print("[FingerPreset] load_presets failed:\n" + traceback.format_exc())
    return _PRESETS


def _write_presets():
    path = _preset_file_path()
    folder = os.path.dirname(path)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(_PRESETS, handle, ensure_ascii=False, indent=2)


def preset_names():
    return sorted(_PRESETS.keys())


def save_preset(name):  # 현재 선택 전체를 이름 프리셋으로 저장/덮어쓰기 + 파일 반영
    name = (name or "").strip()
    if not name:
        return "Enter a preset name."

    entries = _capture_entries()
    if not entries:
        return "No selected finger FK rotation curves."

    overwrite = name in _PRESETS
    _PRESETS[name] = entries
    try:
        _write_presets()
    except Exception:
        return "Save failed:\n" + traceback.format_exc()

    return (
        "{action} preset '{name}'\n"
        "Rotation curves: {count}\n"
        "File: {path}"
    ).format(
        action="Overwrote" if overwrite else "Saved",
        name=name,
        count=len(entries),
        path=_preset_file_path(),
    )


def delete_preset(name):
    name = (name or "").strip()
    if name not in _PRESETS:
        return "Preset '{0}' not found.".format(name)

    del _PRESETS[name]
    try:
        _write_presets()
    except Exception:
        return "Delete failed:\n" + traceback.format_exc()

    return "Deleted preset '{0}'".format(name)


def apply_preset(name):
    name = (name or "").strip()
    return _apply_entries(_PRESETS.get(name, []), "preset '" + name + "'")


def hold_preset(name, start_frame, end_frame, blend_frames):
    name = (name or "").strip()
    return _hold_entries(_PRESETS.get(name, []), start_frame, end_frame, blend_frames, "preset '" + name + "'")


def zero_current_rotation():
    items = _rotation_nodes_for_zeroing()
    if not items:
        return "No selected rotation curves."

    time = _current_time()
    key_count = 0

    for _, _, fcurve in items:
        fcurve.KeyAdd(time, 0.0)
        key_count += 1

    FBSystem().Scene.Evaluate()
    return (
        "Zero current rotation\n"
        "Selected models: {models}\n"
        "Keyed curves: {keys}"
    ).format(
        models=len(_selected_models()),
        keys=key_count,
    )


def zero_range_rotation(start_frame, end_frame):
    items = _rotation_nodes_for_zeroing()
    if not items:
        return "No selected rotation curves."

    first_frame = int(min(start_frame, end_frame))
    last_frame = int(max(start_frame, end_frame))
    start_frame = first_frame
    end_frame = last_frame
    start_time = _frame_time(start_frame)
    end_time = _frame_time(end_frame)
    changed_keys = 0
    edge_keys = 0

    for _, _, fcurve in items:
        for index in _key_indices_in_range(fcurve, start_time, end_time):
            if abs(float(fcurve.KeyGetValue(index))) > 0.000001:
                fcurve.KeySetValue(index, 0.0)
                changed_keys += 1

        fcurve.KeyAdd(start_time, 0.0)
        fcurve.KeyAdd(end_time, 0.0)
        edge_keys += 2

    FBSystem().Scene.Evaluate()
    return (
        "Zero range rotation\n"
        "Frame range: {start} - {end}\n"
        "Changed keys: {changed}\n"
        "Added edge keys: {edges}"
    ).format(
        start=start_frame,
        end=end_frame,
        changed=changed_keys,
        edges=edge_keys,
    )


def zero_all_rotation_keys():
    items = _rotation_nodes_for_selection()
    if not items:
        return "No selected rotation curves."

    changed_keys = 0
    scanned_keys = 0

    for _, _, fcurve in items:
        for index, _ in enumerate(fcurve.Keys):
            scanned_keys += 1
            if abs(float(fcurve.KeyGetValue(index))) > 0.000001:
                fcurve.KeySetValue(index, 0.0)
                changed_keys += 1

    FBSystem().Scene.Evaluate()
    return (
        "Zero all rotation keys\n"
        "Scanned keys: {scanned}\n"
        "Changed keys: {changed}"
    ).format(
        scanned=scanned_keys,
        changed=changed_keys,
    )


class FingerPresetTool(object):
    def __init__(self):
        self.tool = FBCreateUniqueTool(_TOOL_NAME)
        self.tool.StartSizeX = 520
        self.tool.StartSizeY = 520

        self.start_edit = FBEditNumber()
        self.start_edit.Value = float(START_FRAME)

        self.end_edit = FBEditNumber()
        self.end_edit.Value = float(END_FRAME)

        self.blend_edit = FBEditNumber()
        self.blend_edit.Value = float(BLEND_FRAMES)

        self.preset_name_edit = FBEdit()  # 프리셋 이름 입력
        self.preset_name_edit.Text = ""

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "Finger FK 컨트롤을 multi-select(Ctrl+클릭) 하세요.\n"
            "A/B/C: 세션 임시 슬롯. Preset: 이름으로 파일 저장(영구).\n"
            "Zero 버튼은 선택한 컨트롤의 rotation을 0으로 키잉합니다."
        )

        load_presets()
        self._build_ui()

    def _add_region(self, name, x, y, w, h, control):
        self.tool.AddRegion(
            name,
            name,
            FBAddRegionParam(x, FBAttachType.kFBAttachLeft, ""),
            FBAddRegionParam(y, FBAttachType.kFBAttachTop, ""),
            FBAddRegionParam(w, FBAttachType.kFBAttachNone, ""),
            FBAddRegionParam(h, FBAttachType.kFBAttachNone, ""),
        )
        self.tool.SetControl(name, control)

    def _label(self, text):
        label = FBLabel()
        label.Caption = text
        return label

    def _button(self, text, callback):
        button = FBButton()
        button.Caption = text
        button.OnClick.Add(callback)
        return button

    def _build_ui(self):
        self._add_region("start_label", 10, 10, 90, 22, self._label("Start"))
        self._add_region("start_edit", 105, 10, 90, 22, self.start_edit)
        self._add_region("end_label", 210, 10, 80, 22, self._label("End"))
        self._add_region("end_edit", 295, 10, 90, 22, self.end_edit)
        self._add_region("blend_label", 395, 10, 50, 22, self._label("Blend"))
        self._add_region("blend_edit", 445, 10, 45, 22, self.blend_edit)

        self._add_region("cap_a", 10, 52, 150, 28, self._button("Capture A", self._capture_a))
        self._add_region("apply_a", 175, 52, 150, 28, self._button("Apply A", self._apply_a))
        self._add_region("hold_a", 340, 52, 150, 28, self._button("A Hold", self._hold_a))

        self._add_region("cap_b", 10, 90, 150, 28, self._button("Capture B", self._capture_b))
        self._add_region("apply_b", 175, 90, 150, 28, self._button("Apply B", self._apply_b))
        self._add_region("hold_b", 340, 90, 150, 28, self._button("B Hold", self._hold_b))

        self._add_region("cap_c", 10, 128, 150, 28, self._button("Capture C", self._capture_c))
        self._add_region("apply_c", 175, 128, 150, 28, self._button("Apply C", self._apply_c))
        self._add_region("hold_c", 340, 128, 150, 28, self._button("C Hold", self._hold_c))

        self._add_region("zero_current", 10, 175, 150, 28, self._button("Zero Current", self._zero_current))
        self._add_region("zero_range", 175, 175, 150, 28, self._button("Zero Range", self._zero_range))
        self._add_region("zero_all", 340, 175, 150, 28, self._button("Zero All Keys", self._zero_all))

        self._add_region("preset_label", 10, 215, 55, 22, self._label("Preset"))
        self._add_region("preset_name", 70, 215, 420, 22, self.preset_name_edit)

        self._add_region("preset_save", 10, 245, 150, 28, self._button("Save / Overwrite", self._save_preset))
        self._add_region("preset_apply", 175, 245, 150, 28, self._button("Apply Preset", self._apply_preset))
        self._add_region("preset_hold", 340, 245, 150, 28, self._button("Hold Preset", self._hold_preset))

        self._add_region("preset_delete", 10, 283, 150, 28, self._button("Delete Preset", self._delete_preset))
        self._add_region("preset_list", 175, 283, 150, 28, self._button("List Presets", self._list_presets))

        self._add_region("status", 10, 325, 480, 170, self.status)

    def _range(self):
        return int(self.start_edit.Value), int(self.end_edit.Value), int(self.blend_edit.Value)

    def _set_status(self, message):
        self.status.Text = message
        print("[FingerPreset] " + message.replace("\n", " | "))

    def _capture(self, slot):
        self._set_status(capture_slot(slot))

    def _apply(self, slot):
        self._set_status(apply_slot(slot))

    def _hold(self, slot):
        start, end, blend = self._range()
        self._set_status(hold_slot(slot, start, end, blend))

    def _zero_current(self, control, event):
        self._set_status(zero_current_rotation())

    def _zero_range(self, control, event):
        start, end, _ = self._range()
        self._set_status(zero_range_rotation(start, end))

    def _zero_all(self, control, event):
        self._set_status(zero_all_rotation_keys())

    def _preset_name(self):
        return self.preset_name_edit.Text

    def _save_preset(self, control, event):
        self._set_status(save_preset(self._preset_name()))

    def _apply_preset(self, control, event):
        self._set_status(apply_preset(self._preset_name()))

    def _hold_preset(self, control, event):
        start, end, blend = self._range()
        self._set_status(hold_preset(self._preset_name(), start, end, blend))

    def _delete_preset(self, control, event):
        self._set_status(delete_preset(self._preset_name()))

    def _list_presets(self, control, event):
        names = preset_names()
        body = "\n".join(names) if names else "(none)"
        self._set_status("Presets ({0}):\n{1}".format(len(names), body))

    def _capture_a(self, control, event):
        self._capture("A")

    def _apply_a(self, control, event):
        self._apply("A")

    def _hold_a(self, control, event):
        self._hold("A")

    def _capture_b(self, control, event):
        self._capture("B")

    def _apply_b(self, control, event):
        self._apply("B")

    def _hold_b(self, control, event):
        self._hold("B")

    def _capture_c(self, control, event):
        self._capture("C")

    def _apply_c(self, control, event):
        self._apply("C")

    def _hold_c(self, control, event):
        self._hold("C")

    def show(self):
        ShowTool(self.tool)


def main() -> None:
    global _TOOL_REF
    _TOOL_REF = FingerPresetTool()
    _TOOL_REF.show()
    print("[FingerPreset] Tool opened.")


if __name__ != "finger_preset_tool":
    try:
        main()
    except Exception:
        error = traceback.format_exc()
        print(error)
        FBMessageBox("Finger Preset Error", error, "OK")
