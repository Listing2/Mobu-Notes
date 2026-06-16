# Mobu 2025 — 선택한 CR 컨트롤의 FCurve 노이즈를 구간 smoothing
# 실행: Window → Python Editor → Open → Execute

from pyfbsdk import *  # noqa: F403
from pyfbsdk_additions import *  # noqa: F403


# =========================
# 설정
# =========================
START_FRAME = 0
END_FRAME = 120

# "rotation", "translation", "all"
CHANNEL_MODE = "rotation"

# 0.0 = 변화 없음, 1.0 = moving average 완전 적용
STRENGTH = 0.5

# 한 키 기준 좌우 몇 개 키를 평균에 포함할지
RADIUS = 2

# 반복 횟수. 강하게 밀고 싶으면 2~3.
PASSES = 1

# True면 구간 첫/끝 키는 유지해서 앞뒤 구간과 덜 튐.
KEEP_RANGE_EDGES = True


def _clamp(value, min_value, max_value):  # 값 범위 제한
    return max(min_value, min(max_value, value))


def _frame_time(frame):  # 프레임 번호를 FBTime으로 변환
    return FBTime(0, 0, 0, int(frame))


def _time_ticks(time_value):  # FBTime 비교용 tick 추출
    return time_value.Get()


def _selected_models():  # 현재 선택된 모델 목록 반환
    models = FBModelList()
    FBGetSelectedModels(models)
    return list(models)


def _iter_animation_nodes(node, path=""):  # AnimationNode 트리 순회
    if node is None:
        return

    name = getattr(node, "Name", "") or ""
    next_path = (path + "/" + name).lower()

    yield node, next_path

    for child in node.Nodes:
        for item in _iter_animation_nodes(child, next_path):
            yield item


def _channel_matches(path):  # 설정된 채널 종류만 처리
    mode = CHANNEL_MODE.lower().strip()
    if mode == "all":
        return True
    if mode == "rotation":
        return "rotation" in path or "rotate" in path
    if mode == "translation":
        return "translation" in path or "translate" in path
    return True


def _key_indices_in_range(fcurve, start_ticks, end_ticks):  # 구간 안 키 인덱스 수집
    indices = []
    for index, key in enumerate(fcurve.Keys):
        tick = _time_ticks(key.Time)
        if start_ticks <= tick <= end_ticks:
            indices.append(index)
    return indices


def _smooth_fcurve(fcurve, start_ticks, end_ticks):  # 단일 FCurve smoothing
    indices = _key_indices_in_range(fcurve, start_ticks, end_ticks)
    if len(indices) < 3:
        return 0

    strength = _clamp(float(STRENGTH), 0.0, 1.0)
    radius = max(1, int(RADIUS))
    passes = max(1, int(PASSES))

    changed = 0

    for _ in range(passes):
        original = [float(fcurve.KeyGetValue(index)) for index in indices]
        next_values = list(original)

        for local_index, current_value in enumerate(original):
            if KEEP_RANGE_EDGES and local_index in (0, len(original) - 1):
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


def clean_selected_noise():  # 선택 모델의 matching FCurve smoothing 실행
    start_frame = int(min(START_FRAME, END_FRAME))
    end_frame = int(max(START_FRAME, END_FRAME))
    start_ticks = _time_ticks(_frame_time(start_frame))
    end_ticks = _time_ticks(_frame_time(end_frame))

    selected = _selected_models()
    if not selected:
        FBMessageBox("Noise Cleaner", "CR 컨트롤이나 모델을 선택한 뒤 실행하세요.", "OK")
        return

    curve_count = 0
    key_count = 0

    for model in selected:
        for node, path in _iter_animation_nodes(model.AnimationNode):
            if not _channel_matches(path):
                continue

            fcurve = node.FCurve
            if fcurve is None:
                continue

            changed = _smooth_fcurve(fcurve, start_ticks, end_ticks)
            if changed:
                curve_count += 1
                key_count += changed

    message = (
        "대상: {models}개 선택 모델\n"
        "구간: {start}~{end} frame\n"
        "채널: {channel}\n"
        "수정: {curves} curves / {keys} keys"
    ).format(
        models=len(selected),
        start=start_frame,
        end=end_frame,
        channel=CHANNEL_MODE,
        curves=curve_count,
        keys=key_count,
    )

    print("[NoiseCleaner] " + message.replace("\n", " | "))
    FBMessageBox("Noise Cleaner", message, "OK")


def main() -> None:  # 스크립트 진입점
    clean_selected_noise()


if __name__ in ("__main__", "__builtin__"):
    main()
