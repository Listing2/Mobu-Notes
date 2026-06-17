# Mobu 2025 - blend selected upper-body controls toward a target pose
# Run: Window -> Python Editor -> Open -> Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403
import traceback


START_FRAME = 0
TARGET_FRAME = 15
END_FRAME = 30
STRENGTH = 0.75

_TOOL_NAME = "Mobu Pose Blend"
_TOOL_REF = None
_EXCLUDE_WORDS = (
    "root",
    "hips",
    "hip",
    "pelvis",
    "foot",
    "feet",
    "toe",
    "ankle",
    "leg",
    "knee",
)


def _clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def _frame_time(frame):
    return FBTime(0, 0, 0, int(frame))


def _time_ticks(time_value):
    return time_value.Get()


def _current_frame():
    try:
        return int(FBSystem().LocalTime.GetFrame())
    except Exception:
        return 0


def _selected_models():
    models = FBModelList()
    FBGetSelectedModels(models)
    return list(models)


def _iter_animation_nodes(node, path=""):
    if node is None:
        return

    name = getattr(node, "Name", "") or ""
    next_path = (path + "/" + name).lower()

    yield node, next_path

    for child in node.Nodes:
        for item in _iter_animation_nodes(child, next_path):
            yield item


def _is_excluded(model_name, path):
    text = (model_name + "/" + path).lower()
    return any(word in text for word in _EXCLUDE_WORDS)


def _rotation_curves_for_selection():
    items = []
    skipped = 0

    for model in _selected_models():
        model_name = model.Name
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not ("rotation" in path or "rotate" in path):
                continue

            if _is_excluded(model_name, path):
                skipped += 1
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            items.append((model_name, path, fcurve))

    return items, skipped


def _key_indices_in_range(fcurve, start_ticks, end_ticks):
    indices = []
    for index, key in enumerate(fcurve.Keys):
        tick = _time_ticks(key.Time)
        if start_ticks <= tick <= end_ticks:
            indices.append(index)
    return indices


def _falloff_weight(frame, start_frame, target_frame, end_frame):
    if frame <= start_frame or frame >= end_frame:
        return 0.0

    if frame == target_frame:
        return 1.0

    if frame < target_frame:
        span = float(max(1, target_frame - start_frame))
        return _clamp((frame - start_frame) / span, 0.0, 1.0)

    span = float(max(1, end_frame - target_frame))
    return _clamp((end_frame - frame) / span, 0.0, 1.0)


def blend_selected_to_target(start_frame, target_frame, end_frame, strength):
    start_frame = int(start_frame)
    target_frame = int(target_frame)
    end_frame = int(end_frame)

    start = min(start_frame, end_frame)
    end = max(start_frame, end_frame)
    target = _clamp(target_frame, start, end)
    strength = _clamp(float(strength), 0.0, 1.0)

    start_ticks = _time_ticks(_frame_time(start))
    end_ticks = _time_ticks(_frame_time(end))
    target_time = _frame_time(target)

    items, skipped = _rotation_curves_for_selection()
    if not items:
        return "No selected upper-body rotation curves.\nRoot / hips / foot controls are ignored."

    changed_curves = 0
    changed_keys = 0
    target_keys = 0

    for model_name, path, fcurve in items:
        target_value = float(fcurve.Evaluate(target_time))
        indices = _key_indices_in_range(fcurve, start_ticks, end_ticks)

        if not indices:
            continue

        curve_changed = False
        for index in indices:
            key = fcurve.Keys[index]
            try:
                frame = int(key.Time.GetFrame())
            except Exception:
                frame = target

            weight = _falloff_weight(frame, start, target, end) * strength
            if weight <= 0.0:
                continue

            original = float(fcurve.KeyGetValue(index))
            new_value = original + (target_value - original) * weight

            if abs(new_value - original) > 0.000001:
                fcurve.KeySetValue(index, new_value)
                changed_keys += 1
                curve_changed = True

        fcurve.KeyAdd(target_time, target_value)
        target_keys += 1

        if curve_changed:
            changed_curves += 1

    FBSystem().Scene.Evaluate()

    return (
        "Pose blend\n"
        "Frame range: {start} - {end}\n"
        "Target frame: {target}\n"
        "Strength: {strength}\n"
        "Rotation curves: {curves}\n"
        "Changed: {changed_curves} curves / {changed_keys} keys\n"
        "Target keys added: {target_keys}\n"
        "Excluded lower/root curves: {skipped}"
    ).format(
        start=start,
        end=end,
        target=target,
        strength=strength,
        curves=len(items),
        changed_curves=changed_curves,
        changed_keys=changed_keys,
        target_keys=target_keys,
        skipped=skipped,
    )


def scan_selection():
    items, skipped = _rotation_curves_for_selection()
    if not items:
        return "No selected upper-body rotation curves.\nRoot / hips / foot controls are ignored."

    preview = []
    for model_name, path, _ in items[:20]:
        preview.append("{0}: {1}".format(model_name, path.strip("/")))

    return (
        "Pose blend selection\n"
        "Rotation curves: {curves}\n"
        "Excluded lower/root curves: {skipped}\n"
        "{preview}"
    ).format(
        curves=len(items),
        skipped=skipped,
        preview="\n".join(preview),
    )


class PoseBlendTool(object):
    def __init__(self):
        self.tool = FBCreateUniqueTool(_TOOL_NAME)
        self.tool.StartSizeX = 520
        self.tool.StartSizeY = 330

        current = _current_frame()

        self.start_edit = FBEditNumber()
        self.start_edit.Value = float(current - 15 if current else START_FRAME)

        self.target_edit = FBEditNumber()
        self.target_edit.Value = float(current if current else TARGET_FRAME)

        self.end_edit = FBEditNumber()
        self.end_edit.Value = float(current + 15 if current else END_FRAME)

        self.strength_edit = FBEditNumber()
        self.strength_edit.Value = float(STRENGTH)

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "Select upper-body / arm / head controls.\n"
            "Set a target pose key at Target frame, then blend Start-End toward it.\n"
            "Root / hips / legs / feet are ignored by name."
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
        self._add_region("start_edit", 105, 10, 80, 22, self.start_edit)
        self._add_region("target_label", 195, 10, 90, 22, self._label("Target"))
        self._add_region("target_edit", 285, 10, 80, 22, self.target_edit)
        self._add_region("end_label", 375, 10, 45, 22, self._label("End"))
        self._add_region("end_edit", 420, 10, 70, 22, self.end_edit)

        self._add_region("strength_label", 10, 45, 90, 22, self._label("Strength"))
        self._add_region("strength_edit", 105, 45, 80, 22, self.strength_edit)
        self._add_region("note", 195, 45, 290, 22, self._label("Rotation only / lower body ignored"))

        self._add_region("scan", 10, 85, 150, 30, self._button("Scan Selection", self._scan))
        self._add_region("blend", 175, 85, 150, 30, self._button("Blend To Target", self._blend))
        self._add_region("current", 340, 85, 150, 30, self._button("Use Current Frame", self._use_current))

        self._add_region("status", 10, 130, 480, 150, self.status)

    def _settings(self):
        return (
            int(self.start_edit.Value),
            int(self.target_edit.Value),
            int(self.end_edit.Value),
            _clamp(float(self.strength_edit.Value), 0.0, 1.0),
        )

    def _set_status(self, message):
        self.status.Text = message
        print("[PoseBlend] " + message.replace("\n", " | "))

    def _scan(self, control, event):
        self._set_status(scan_selection())

    def _blend(self, control, event):
        start, target, end, strength = self._settings()
        self._set_status(blend_selected_to_target(start, target, end, strength))

    def _use_current(self, control, event):
        current = _current_frame()
        self.target_edit.Value = float(current)
        self.start_edit.Value = float(current - 15)
        self.end_edit.Value = float(current + 15)
        self._set_status("Frame range set around current frame: {0}".format(current))

    def show(self):
        ShowTool(self.tool)


def main() -> None:
    global _TOOL_REF
    _TOOL_REF = PoseBlendTool()
    _TOOL_REF.show()
    print("[PoseBlend] Tool opened.")


if __name__ != "pose_blend_tool":
    try:
        main()
    except Exception:
        error = traceback.format_exc()
        print(error)
        FBMessageBox("Pose Blend Error", error, "OK")
