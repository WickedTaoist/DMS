def should_keep_frame(frame_index: int, src_fps: float, target_fps: float) -> bool:
    """Keep a frame according to simple fps down-sampling."""
    if target_fps <= 0 or src_fps <= 0 or target_fps >= src_fps:
        return True
    step = int(round(src_fps / target_fps))
    step = max(1, step)
    return frame_index % step == 0
