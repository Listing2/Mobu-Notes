# Mobu 2025 - finger FK pose preset tool
# Run: Window -> Python Editor -> Open -> Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403
import traceback


START_FRAME = 0
END_FRAME = 30
BLEND_FRAMES = 2

_TOOL_NAME = "Mobu Finger Presets"
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


class FingerPresetTool(object):
    def __init__(self):
        self.tool = FBCreateUniqueTool(_TOOL_NAME)
        self.tool.StartSizeX = 520
        self.tool.StartSizeY = 360

        self.start_edit = FBEditNumber()
        self.start_edit.Value = float(START_FRAME)

        self.end_edit = FBEditNumber()
        self.end_edit.Value = float(END_FRAME)

        self.blend_edit = FBEditNumber()
        self.blend_edit.Value = float(BLEND_FRAMES)

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "Select finger FK controls in a stable order.\n"
            "Pose fingers, Capture A/B/C, then Apply or Hold the same selection.\n"
            "Use for Fist / Open / Index Point / Grip style poses."
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
        self._add_region("start_label", 10, 10, 90, 22, self._label("Start frame"))
        self._add_region("start_edit", 105, 10, 90, 22, self.start_edit)
        self._add_region("end_label", 210, 10, 80, 22, self._label("End frame"))
        self._add_region("end_edit", 295, 10, 90, 22, self.end_edit)
        self._add_region("blend_label", 395, 10, 50, 22, self._label("Blend"))
        self._add_region("blend_edit", 445, 10, 45, 22, self.blend_edit)

        self._add_region("cap_a", 10, 52, 150, 28, self._button("Capture A", self._capture_a))
        self._add_region("apply_a", 175, 52, 150, 28, self._button("Apply A", self._apply_a))
        self._add_region("hold_a", 340, 52, 150, 28, self._button("Hold A", self._hold_a))

        self._add_region("cap_b", 10, 90, 150, 28, self._button("Capture B", self._capture_b))
        self._add_region("apply_b", 175, 90, 150, 28, self._button("Apply B", self._apply_b))
        self._add_region("hold_b", 340, 90, 150, 28, self._button("Hold B", self._hold_b))

        self._add_region("cap_c", 10, 128, 150, 28, self._button("Capture C", self._capture_c))
        self._add_region("apply_c", 175, 128, 150, 28, self._button("Apply C", self._apply_c))
        self._add_region("hold_c", 340, 128, 150, 28, self._button("Hold C", self._hold_c))

        self._add_region("status", 10, 175, 480, 135, self.status)

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
