"""
时间工具模块 / Time utility helpers.

本文件用于保存与帧号、时间戳转换相关的基础函数，
避免在多个模块里重复写相同逻辑。

This module stores helper functions for frame/time conversions,
so the same logic is not duplicated across multiple modules.
"""


def frame_to_timestamp_ms(frame_index: int, fps: float) -> int:
    """
    将帧序号转换为毫秒时间戳 / Convert frame index to millisecond timestamp.

    Args:
        frame_index: 当前帧在原始视频中的序号。
        fps: 原始视频的帧率。

    Returns:
        毫秒单位的时间戳；若 FPS 非法则返回 0。
        Timestamp in milliseconds; returns 0 when FPS is invalid.
    """
    # 如果 FPS 无效，则无法进行可靠换算。
    # If FPS is invalid, reliable time conversion is impossible.
    if fps <= 0:
        return 0

    # 帧号 / FPS = 秒数，再乘以 1000 转成毫秒。
    # frame_index / FPS gives seconds, then multiply by 1000 for milliseconds.
    return int((frame_index / fps) * 1000.0)
