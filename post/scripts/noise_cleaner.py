# Mobu 2025 - selected source / CR FCurve noise cleaner tool
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
SPIKE_THRESHOLD = 20.0
BLEND_FRAMES = 2

_TOOL_NAME = "Mobu Noise Cleaner"
_TOOL_REF = None
_BACKUP = {}


def _clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def _frame_time(frame):
    return FBTime(0, 0, 0, int(frame))


def _time_ticks(time_value):
    return time_value.Get()


def _time_to_frame(time_value):
    try:
        return int(time_value.GetFrame())
    except Exception:
        return _time_ticks(time_value)


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


def _flatten_fcurve(fcurve, start_time, start_ticks, end_ticks):
    indices = _key_indices_in_range(fcurve, start_ticks, end_ticks)
    if not indices:
        return 0

    hold_value = float(fcurve.Evaluate(start_time))
    changed = 0

    for index in indices:
        old_value = float(fcurve.KeyGetValue(index))
        if abs(old_value - hold_value) > 0.000001:
            fcurve.KeySetValue(index, hold_value)
            changed += 1

    return changed


def _spike_indices(fcurve, start_ticks, end_ticks, threshold):
    indices = _key_indices_in_range(fcurve, start_ticks, end_ticks)
    if len(indices) < 3:
        return []

    spikes = []
    values = [float(fcurve.KeyGetValue(index)) for index in indices]

    for local_index in range(1, len(indices) - 1):
        prev_value = values[local_index - 1]
        current_value = values[local_index]
        next_value = values[local_index + 1]
        neighbor_average = (prev_value + next_value) * 0.5

        if abs(current_value - neighbor_average) >= threshold:
            spikes.append((indices[local_index], neighbor_average))

    return spikes


def scan_selected_spikes(start_frame, end_frame, channel_mode, threshold):
    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    start_ticks = _time_ticks(_frame_time(start_frame))
    end_ticks = _time_ticks(_frame_time(end_frame))
    threshold = abs(float(threshold))

    selected = _selected_models()
    if not selected:
        return "No selected source bone / CR control."

    scanned_curves = 0
    hit_lines = []

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path, channel_mode):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            scanned_curves += 1
            spikes = _spike_indices(fcurve, start_ticks, end_ticks, threshold)
            if spikes:
                frames = []
                for index, _ in spikes[:8]:
                    frames.append(str(_time_to_frame(fcurve.Keys[index].Time)))
                hit_lines.append("{name}: {count} spikes @ {frames}".format(
                    name=path.strip("/") or model.Name,
                    count=len(spikes),
                    frames=", ".join(frames),
                ))

    if not hit_lines:
        return "Spike scan\nScanned curves: {0}\nNo spikes over threshold {1}.".format(
            scanned_curves,
            threshold,
        )

    return "Spike scan\nScanned curves: {0}\n{1}".format(
        scanned_curves,
        "\n".join(hit_lines[:30]),
    )


def fix_selected_spikes(start_frame, end_frame, channel_mode, threshold):
    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    start_ticks = _time_ticks(_frame_time(start_frame))
    end_ticks = _time_ticks(_frame_time(end_frame))
    threshold = abs(float(threshold))

    selected = _selected_models()
    if not selected:
        return "No selected source bone / CR control."

    scanned_curves = 0
    changed_curves = 0
    changed_keys = 0

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path, channel_mode):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            scanned_curves += 1
            spikes = _spike_indices(fcurve, start_ticks, end_ticks, threshold)
            if not spikes:
                continue

            changed_curves += 1
            for index, replacement in spikes:
                fcurve.KeySetValue(index, replacement)
                changed_keys += 1

    return (
        "Spike fix\n"
        "Selected models: {models}\n"
        "Frame range: {start} - {end}\n"
        "Channel: {channel}\n"
        "Threshold: {threshold}\n"
        "Scanned curves: {scanned}\n"
        "Changed: {curves} curves / {keys} keys"
    ).format(
        models=len(selected),
        start=start_frame,
        end=end_frame,
        channel=channel_mode,
        threshold=threshold,
        scanned=scanned_curves,
        curves=changed_curves,
        keys=changed_keys,
    )


def flatten_selected_range(start_frame, end_frame, channel_mode):
    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    start_time = _frame_time(start_frame)
    start_ticks = _time_ticks(start_time)
    end_ticks = _time_ticks(_frame_time(end_frame))

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
            changed = _flatten_fcurve(fcurve, start_time, start_ticks, end_ticks)
            if changed:
                curve_count += 1
                key_count += changed

    return (
        "Flatten selected range\n"
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


def hold_selected_range(start_frame, end_frame, channel_mode, blend_frames):
    start_frame = int(min(start_frame, end_frame))
    end_frame = int(max(start_frame, end_frame))
    blend_frames = max(0, int(blend_frames))

    pre_frame = start_frame - blend_frames
    post_frame = end_frame + blend_frames

    start_time = _frame_time(start_frame)
    end_time = _frame_time(end_frame)
    pre_time = _frame_time(pre_frame)
    post_time = _frame_time(post_frame)

    selected = _selected_models()
    if not selected:
        return "No selected source bone / CR control."

    curve_count = 0
    key_count = 0

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path, channel_mode):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            pre_value = float(fcurve.Evaluate(pre_time))
            hold_value = float(fcurve.Evaluate(start_time))
            post_value = float(fcurve.Evaluate(post_time))

            fcurve.KeyAdd(pre_time, pre_value)
            fcurve.KeyAdd(start_time, hold_value)
            fcurve.KeyAdd(end_time, hold_value)
            fcurve.KeyAdd(post_time, post_value)

            curve_count += 1
            key_count += 4

    return (
        "Hold keys created\n"
        "Selected models: {models}\n"
        "Hold: {start} - {end}\n"
        "Blend frames: {blend}\n"
        "Channel: {channel}\n"
        "Added: {curves} curves / {keys} keys"
    ).format(
        models=len(selected),
        start=start_frame,
        end=end_frame,
        blend=blend_frames,
        channel=channel_mode,
        curves=curve_count,
        keys=key_count,
    )


def backup_selected_curves(channel_mode):
    global _BACKUP
    selected = _selected_models()
    if not selected:
        return "No selected source bone / CR control."

    _BACKUP = {}
    curve_count = 0
    key_count = 0

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path, channel_mode):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            values = []
            for index, _ in enumerate(fcurve.Keys):
                values.append((index, float(fcurve.KeyGetValue(index))))

            if values:
                _BACKUP[fcurve] = values
                curve_count += 1
                key_count += len(values)

    return "Backup saved\nCurves: {0}\nKeys: {1}".format(curve_count, key_count)


def restore_backup():
    if not _BACKUP:
        return "No backup in this tool session."

    curve_count = 0
    key_count = 0

    for fcurve, values in _BACKUP.items():
        curve_count += 1
        for index, value in values:
            if index < len(fcurve.Keys):
                fcurve.KeySetValue(index, value)
                key_count += 1

    return "Backup restored\nCurves: {0}\nKeys: {1}".format(curve_count, key_count)


class NoiseCleanerTool(object):
    def __init__(self):
        self.tool = FBCreateUniqueTool(_TOOL_NAME)
        self.tool.StartSizeX = 520
        self.tool.StartSizeY = 545

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

        self.spike_edit = FBEditNumber()
        self.spike_edit.Value = float(SPIKE_THRESHOLD)

        self.blend_edit = FBEditNumber()
        self.blend_edit.Value = float(BLEND_FRAMES)

        self.status = FBMemo()
        self.status.ReadOnly = True
        self.status.Text = (
            "소스 본 또는 CR 컨트롤을 하나 이상 선택한 뒤 버튼을 누르세요.\n"
            "소스 클린업은 retarget 전, CR 클린업은 Plot to CR 후에 사용합니다.\n"
            "Clean=잔떨림 완화, Spike=튀는 키, Flatten/Hold=구간 고정."
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

        self._add_region("strength_label", 10, 42, 90, 22, self._label("Strength"))
        self._add_region("strength_edit", 105, 42, 90, 22, self.strength_edit)
        self._add_region("radius_label", 210, 42, 80, 22, self._label("Radius"))
        self._add_region("radius_edit", 295, 42, 90, 22, self.radius_edit)

        self._add_region("passes_label", 10, 74, 90, 22, self._label("Passes"))
        self._add_region("passes_edit", 105, 74, 90, 22, self.passes_edit)
        self._add_region("edge_note", 210, 74, 220, 22, self._label("Keep edge keys"))

        self._add_region("spike_label", 10, 106, 90, 22, self._label("Spike Threshold"))
        self._add_region("spike_edit", 105, 106, 90, 22, self.spike_edit)
        self._add_region("blend_label", 210, 106, 80, 22, self._label("Blend"))
        self._add_region("blend_edit", 295, 106, 90, 22, self.blend_edit)

        self._add_region("backup", 10, 142, 150, 28, self._button("Backup All", self._backup_all))
        self._add_region("restore", 175, 142, 150, 28, self._button("Restore Backup", self._restore_backup))
        self._add_region("scan", 340, 142, 150, 28, self._button("Scan Spikes", self._scan_spikes))

        self._add_region("clean_rot", 10, 180, 150, 28, self._button("Clean Rotation", self._clean_rotation))
        self._add_region("clean_trans", 175, 180, 150, 28, self._button("Clean Translation", self._clean_translation))
        self._add_region("clean_all", 340, 180, 150, 28, self._button("Clean All", self._clean_all))

        self._add_region("spike_fix", 10, 218, 150, 28, self._button("Fix Spikes All", self._fix_spikes_all))
        self._add_region("flat_all", 175, 218, 150, 28, self._button("Flatten All", self._flatten_all))
        self._add_region("hold_all", 340, 218, 150, 28, self._button("Hold Keys All", self._hold_all))

        self._add_region("flat_rot", 10, 256, 150, 28, self._button("Flatten Rotation", self._flatten_rotation))
        self._add_region("flat_trans", 175, 256, 150, 28, self._button("Flatten Translation", self._flatten_translation))
        self._add_region("hold_rot", 340, 256, 150, 28, self._button("Hold Rotation", self._hold_rotation))

        self._add_region("status", 10, 300, 480, 195, self.status)

    def _settings(self):
        return (
            int(self.start_edit.Value),
            int(self.end_edit.Value),
            _clamp(float(self.strength_edit.Value), 0.0, 1.0),
            max(1, int(self.radius_edit.Value)),
            max(1, int(self.passes_edit.Value)),
            True,
        )

    def _spike_threshold(self):
        return max(0.0, float(self.spike_edit.Value))

    def _blend_frames(self):
        return max(0, int(self.blend_edit.Value))

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

    def _flatten(self, mode):
        start, end, strength, radius, passes, keep_edges = self._settings()
        message = flatten_selected_range(start, end, mode)
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))
        FBSystem().Scene.Evaluate()

    def _flatten_rotation(self, control, event):
        self._flatten("rotation")

    def _flatten_translation(self, control, event):
        self._flatten("translation")

    def _flatten_all(self, control, event):
        self._flatten("all")

    def _scan_spikes(self, control, event):
        start, end, strength, radius, passes, keep_edges = self._settings()
        message = scan_selected_spikes(start, end, "all", self._spike_threshold())
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))

    def _fix_spikes_all(self, control, event):
        start, end, strength, radius, passes, keep_edges = self._settings()
        message = fix_selected_spikes(start, end, "all", self._spike_threshold())
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))
        FBSystem().Scene.Evaluate()

    def _hold(self, mode):
        start, end, strength, radius, passes, keep_edges = self._settings()
        message = hold_selected_range(start, end, mode, self._blend_frames())
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))
        FBSystem().Scene.Evaluate()

    def _hold_all(self, control, event):
        self._hold("all")

    def _hold_rotation(self, control, event):
        self._hold("rotation")

    def _backup_all(self, control, event):
        message = backup_selected_curves("all")
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))

    def _restore_backup(self, control, event):
        message = restore_backup()
        self.status.Text = message
        print("[NoiseCleaner] " + message.replace("\n", " | "))
        FBSystem().Scene.Evaluate()

    def show(self):
        ShowTool(self.tool)


def main() -> None:
    global _TOOL_REF
    _TOOL_REF = NoiseCleanerTool()
    _TOOL_REF.show()
    print("[NoiseCleaner] Tool opened.")


if __name__ != "noise_cleaner":
    try:
        main()
    except Exception:
        error = traceback.format_exc()
        print(error)
        FBMessageBox("Noise Cleaner Error", error, "OK")
