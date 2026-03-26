def frame_to_timestamp_ms(frame_index: int, fps: float) -> int:
    if fps <= 0:
        return 0
    return int((frame_index / fps) * 1000.0)
