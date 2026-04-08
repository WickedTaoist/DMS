"""
抽帧模块 / Frame sampling helpers.

本模块负责：
1. 判断某一帧是否应该保留
2. 将解码帧转换成统一 `FrameContext`

This module is responsible for:
1. Deciding whether a frame should be kept
2. Converting decoded frames into unified `FrameContext` objects
"""

from collections.abc import Iterator

from src.detectors.base_detector import FrameContext
from src.io.video_reader import iter_video_frames
from src.utils.time_utils import frame_to_timestamp_ms


def should_keep_frame(frame_index: int, src_fps: float, target_fps: float) -> bool:
    """
    判断当前帧是否应该保留 / Decide whether the current frame should be kept.

    Args:
        frame_index: 原始视频中的帧号。
        src_fps: 原始视频 FPS。
        target_fps: 目标采样 FPS。
    """
    # 若目标 FPS 非法，或目标 FPS 不低于原始 FPS，则保留所有帧。
    # Keep all frames if target FPS is invalid or not lower than source FPS.
    if target_fps <= 0 or src_fps <= 0 or target_fps >= src_fps:
        return True

    # 通过 `src_fps / target_fps` 近似得到采样步长。
    # Approximate the sampling step via `src_fps / target_fps`.
    step = max(1, int(round(src_fps / target_fps)))

    # 仅保留能整除步长的帧。
    # Keep only frames whose index is divisible by the sampling step.
    return frame_index % step == 0


def iter_sampled_frame_contexts(
    video_path: str, video_id: str, target_fps: float
) -> Iterator[FrameContext]:
    """
    迭代采样后的统一帧上下文 / Iterate sampled frames as `FrameContext`.

    这是视频读取层与 detector pipeline 之间的关键桥梁。
    下游模块只消费统一的 `FrameContext`，无需了解 OpenCV 细节。

    This function is the key bridge between raw video I/O and the detector
    pipeline. Downstream modules consume normalized `FrameContext` objects
    without needing to know OpenCV details.
    """
    # 遍历原始视频的逐帧解码结果。
    # Iterate through decoded frames from the source video.
    for frame_index, frame_bgr, src_fps in iter_video_frames(video_path):
        # 若该帧不在采样点上，则跳过。
        # Skip the frame if it does not belong to the sampling schedule.
        if not should_keep_frame(frame_index, src_fps, target_fps):
            continue

        # 将原始帧信息封装为统一上下文，供 detector 直接使用。
        # Wrap the raw frame information into a unified context object.
        yield FrameContext(
            video_id=video_id,
            frame_index=frame_index,
            timestamp_ms=frame_to_timestamp_ms(frame_index, src_fps),
            frame_bgr=frame_bgr,
        )
