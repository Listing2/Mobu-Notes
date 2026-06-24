# Mobu 2025 - finger FK pose preset tool
# Run: Window -> Python Editor -> Open -> Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403
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


def capture_slot(slot_name):
    time = _current_time()
    items = _rotation_nodes_for_selection()
    if not items:
        return "No selected finger FK rotation curves."

    _SLOTS[slot_name] = []
    for model_name, path, fcurve in items:
        _SLOTS[slot_name].append({
            "model": model_name,
            "path": path,
            "value": float(fcurve.Evaluate(time)),
        })

    return "Captured slot {0}\nRotation curves: {1}".format(slot_name, len(_SLOTS[slot_name]))


def _matching_curves(slot_name):
    slot_values = _SLOTS.get(slot_name, [])
    items = _rotation_nodes_for_selection()
    count = min(len(slot_values), len(items))
    matches = []

    for index in range(count):
        matches.append((items[index][2], slot_values[index]["value"]))

    return matches, len(slot_values), len(items)


def apply_slot(slot_name):
    matches, preset_count, selected_count = _matching_curves(slot_name)
    if not matches:
        return "Slot {0} is empty or no matching selection.".format(slot_name)

    time = _current_time()
    key_count = 0
    for fcurve, value in matches:
        fcurve.KeyAdd(time, value)
        key_count += 1

    FBSystem().Scene.Evaluate()
    return (
        "Applied slot {slot}\n"
        "Preset curves: {preset}\n"
        "Selected curves: {selected}\n"
        "Keyed curves: {keys}"
    ).format(
        slot=slot_name,
        preset=preset_count,
        selected=selected_count,
        keys=key_count,
    )


def hold_slot(slot_name, start_frame, end_frame, blend_frames):
    matches, preset_count, selected_count = _matching_curves(slot_name)
    if not matches:
        return "Slot {0} is empty or no matching selection.".format(slot_name)

    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    blend_frames = max(0, int(blend_frames))

    pre_time = _frame_time(start_frame - blend_frames)
    start_time = _frame_time(start_frame)
    end_time = _frame_time(end_frame)
    post_time = _frame_time(end_frame + blend_frames)

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
        "Hold slot {slot}\n"
        "Frame range: {start} - {end}\n"
        "Blend frames: {blend}\n"
        "Preset curves: {preset}\n"
        "Selected curves: {selected}\n"
        "Added keys: {keys}"
    ).format(
        slot=slot_name,
        start=start_frame,
        end=end_frame,
        blend=blend_frames,
        preset=preset_count,
        selected=selected_count,
        keys=key_count,
    )


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
        self.tool.StartSizeY = 410

        self.start_edit = FBEditNumber()
        self.start_edit.Value = float(START_FRAME)

        self.end_edit = FBEditNumber()
        self.end_edit.Value = float(END_FRAME)

        self.blend_edit = FBEditNumber()
        self.blend_edit.Value = float(BLEND_FRAMES)

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "Finger FK 컨트롤을 같은 순서로 선택하세요.\n"
            "손 모양을 만든 뒤 A/B/C에 캡처하고, 같은 선택에 적용/Hold합니다.\n"
            "Zero 버튼은 선택한 컨트롤의 rotation을 0으로 키잉합니다."
        )

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

        self._add_region("status", 10, 220, 480, 135, self.status)

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
