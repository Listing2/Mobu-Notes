# Mobu 2025 — selected source / CR FCurve noise cleaner tool
# Run: Window -> Python Editor -> Open -> Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403
import traceback


START_FRAME = 3730
END_FRAME = 3765
CHANNEL_MODE = "all"
STRENGTH = 0.5
RADIUS = 2
PASSES = 2
KEEP_RANGE_EDGES = True

_TOOL_NAME = "Mobu Noise Cleaner"
_TOOL_REF = None


def _clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def _frame_time(frame):
    return FBTime(0, 0, 0, int(frame))


def _time_ticks(time_value):
    return time_value.Get()


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


def _channel_matches(path, mode):
    mode = mode.lower().strip()
    if mode == "all":
        return True
    if mode == "rotation":
        return "rotation" in path or "rotate" in path
    if mode == "translation":
        return "translation" in path or "translate" in path
    return True


def _key_indices_in_range(fcurve, start_ticks, end_ticks):
    indices = []
    for index, key in enumerate(fcurve.Keys):
        tick = _time_ticks(key.Time)
        if start_ticks <= tick <= end_ticks:
            indices.append(index)
    return indices


def _smooth_fcurve(fcurve, start_ticks, end_ticks, strength, radius, passes, keep_edges):
    indices = _key_indices_in_range(fcurve, start_ticks, end_ticks)
    if len(indices) < 3:
        return 0

    changed = 0

    for _ in range(passes):
        original = [float(fcurve.KeyGetValue(index)) for index in indices]
        next_values = list(original)

        for local_index, current_value in enumerate(original):
            if keep_edges and local_index in (0, len(original) - 1):
                continue

            left = max(0, local_index - radius)
            right = min(len(original), local_index + radius + 1)
            average = sum(original[left:right]) / float(right - left)
            next_values[local_index] = current_value + (average - current_value) * strength

        for local_index, curve_index in enumerate(indices):
            new_value = next_values[local_index]
            if abs(new_value - original[local_index]) > 0.000001:
                fcurve.KeySetValue(curve_index, new_value)
                changed += 1

    return changed


def clean_selected_noise(start_frame, end_frame, channel_mode, strength, radius, passes, keep_edges=True):
    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    start_ticks = _time_ticks(_frame_time(start_frame))
    end_ticks = _time_ticks(_frame_time(end_frame))
    strength = _clamp(float(strength), 0.0, 1.0)
    radius = max(1, int(radius))
    passes = max(1, int(passes))

    selected = _selected_models()
    if not selected:
        return "No selected source bone / CR control."

    curve_count = 0
    key_count = 0
    scanned_curves = 0

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path, channel_mode):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            scanned_curves += 1
            changed = _smooth_fcurve(
                fcurve,
                start_ticks,
                end_ticks,
                strength,
                radius,
                passes,
                keep_edges,
            )
            if changed:
                curve_count += 1
                key_count += changed

    return (
        "Selected models: {models}\n"
        "Frame range: {start} - {end}\n"
        "Channel: {channel}\n"
        "Scanned curves: {scanned}\n"
        "Changed: {curves} curves / {keys} keys"
    ).format(
        models=len(selected),
        start=start_frame,
        end=end_frame,
        channel=channel_mode,
        scanned=scanned_curves,
        curves=curve_count,
        keys=key_count,
    )


class NoiseCleanerTool(object):
    def __init__(self):
        self.tool = FBCreateUniqueTool(_TOOL_NAME)
        self.tool.StartSizeX = 520
        self.tool.StartSizeY = 360

        self.start_edit = FBEditNumber()
        self.start_edit.Value = float(START_FRAME)

        self.end_edit = FBEditNumber()
        self.end_edit.Value = float(END_FRAME)

        self.strength_edit = FBEditNumber()
        self.strength_edit.Value = float(STRENGTH)

        self.radius_edit = FBEditNumber()
        self.radius_edit.Value = float(RADIUS)

        self.passes_edit = FBEditNumber()
        self.passes_edit.Value = float(PASSES)

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "Select source bones or CR controls, then click a clean button.\n"
            "Use Source cleanup before retarget. Use CR cleanup after Plot to CR.\n"
            "Start weak: strength 0.3 - 0.5."
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

        self._add_region("strength_label", 10, 42, 90, 22, self._label("Strength"))
        self._add_region("strength_edit", 105, 42, 90, 22, self.strength_edit)
        self._add_region("radius_label", 210, 42, 80, 22, self._label("Radius"))
        self._add_region("radius_edit", 295, 42, 90, 22, self.radius_edit)

        self._add_region("passes_label", 10, 74, 90, 22, self._label("Passes"))
        self._add_region("passes_edit", 105, 74, 90, 22, self.passes_edit)
        self._add_region("edge_note", 210, 74, 220, 22, self._label("First/last keys are kept"))

        self._add_region("btn_rot", 10, 112, 150, 30, self._button("Clean Rotation", self._clean_rotation))
        self._add_region("btn_trans", 175, 112, 150, 30, self._button("Clean Translation", self._clean_translation))
        self._add_region("btn_all", 340, 112, 150, 30, self._button("Clean All", self._clean_all))

        self._add_region("status", 10, 155, 480, 165, self.status)

    def _settings(self):
        return (
            int(self.start_edit.Value),
            int(self.end_edit.Value),
            _clamp(float(self.strength_edit.Value), 0.0, 1.0),
            max(1, int(self.radius_edit.Value)),
            max(1, int(self.passes_edit.Value)),
            True,
        )

    def _run(self, mode):
        start, end, strength, radius, passes, keep_edges = self._settings()
        message = clean_selected_noise(start, end, mode, strength, radius, passes, keep_edges)
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))
        FBSystem().Scene.Evaluate()

    def _clean_rotation(self, control, event):
        self._run("rotation")

    def _clean_translation(self, control, event):
        self._run("translation")

    def _clean_all(self, control, event):
        self._run("all")

    def show(self):
        ShowTool(self.tool)


def main() -> None:
    global _TOOL_REF
    _TOOL_REF = NoiseCleanerTool()
    _TOOL_REF.show()
    print("[NoiseCleaner] Tool opened.")


try:
    main()
except Exception:
    error = traceback.format_exc()
    print(error)
    FBMessageBox("Noise Cleaner Error", error, "OK")
