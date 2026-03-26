from collections.abc import Iterator

from src.detectors.base_detector import FrameContext
from src.io.video_reader import iter_video_frames
from src.utils.time_utils import frame_to_timestamp_ms


def should_keep_frame(frame_index: int, src_fps: float, target_fps: float) -> bool:
    """Return whether a source frame should be kept for target FPS."""
    if target_fps <= 0 or src_fps <= 0 or target_fps >= src_fps:
        return True
    step = max(1, int(round(src_fps / target_fps)))
    return frame_index % step == 0


def iter_sampled_frame_contexts(
    video_path: str, video_id: str, target_fps: float
) -> Iterator[FrameContext]:
    """
    Decode and sample a video, then emit unified FrameContext objects.

    This function is the single bridge from raw video I/O to detector pipeline,
    so downstream modules do not depend on OpenCV details.
    """
    for frame_index, frame_bgr, src_fps in iter_video_frames(video_path):
        if not should_keep_frame(frame_index, src_fps, target_fps):
            continue
        yield FrameContext(
            video_id=video_id,
            frame_index=frame_index,
            timestamp_ms=frame_to_timestamp_ms(frame_index, src_fps),
            frame_bgr=frame_bgr,
        )
