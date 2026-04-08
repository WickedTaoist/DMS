"""
视频读取模块 / Video I/O helpers.

本模块封装 OpenCV 视频读取相关逻辑，包括：
1. 逐帧解码
2. 目录扫描
3. 视频元信息提取

This module wraps OpenCV-based video reading logic, including:
1. Frame-by-frame decoding
2. Directory scanning
3. Video metadata extraction
"""

from pathlib import Path
from typing import Iterator

import cv2 as cv
import numpy as np
from numpy.typing import NDArray


def iter_video_frames(video_path: str) -> Iterator[tuple[int, NDArray[np.uint8], float]]:
    """
    逐帧迭代视频内容 / Iterate through a video frame by frame.

    Args:
        video_path: 输入视频路径。

    Yields:
        `(frame_index, frame_bgr, source_fps)` 三元组。
        `(frame_index, frame_bgr, source_fps)` tuples.
    """
    # 创建 OpenCV 视频读取对象。
    # Create the OpenCV video capture object.
    cap = cv.VideoCapture(video_path)

    # 若视频无法打开，立即抛出明确错误。
    # Raise a clear error immediately if the video cannot be opened.
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    # 从视频元信息中读取原始 FPS；若失败则退化到 30。
    # Read source FPS from metadata; fall back to 30 when unavailable.
    fps = cap.get(cv.CAP_PROP_FPS) or 30.0

    # 使用手动计数器追踪当前帧号。
    # Track the current frame index with a manual counter.
    idx = 0

    # 持续读取直到视频结束。
    # Keep reading until the video ends.
    while True:
        ok, frame = cap.read()

        # 读取失败通常表示到达视频末尾。
        # A failed read usually means the end of the video.
        if not ok:
            break

        # 按 OpenCV 约定保留 BGR ndarray，不在此处做格式变换。
        # Keep the raw BGR ndarray following OpenCV conventions.
        yield idx, frame, float(fps)

        # 帧号自增。
        # Increment the frame counter.
        idx += 1

    # 释放底层句柄，避免资源泄漏。
    # Release the underlying handle to avoid resource leakage.
    cap.release()


def list_videos(video_dir: str) -> list[str]:
    """
    扫描目录中的常见视频文件 / List common video files in a directory.

    该函数是早期的通用视频扫描接口，目前仍保留供兼容使用。
    This is an earlier generic scanner kept for compatibility.
    """
    # 定义允许的视频扩展名。
    # Define the supported video file extensions.
    exts = {".mp4", ".avi", ".mov", ".mkv"}

    # 收集命中的视频路径。
    # Collect matched video paths.
    paths = []
    for path in Path(video_dir).glob("*"):
        if path.suffix.lower() in exts:
            paths.append(str(path))
    return sorted(paths)


def list_videos_by_glob(video_dir: str, video_glob: str) -> list[str]:
    """
    按 glob 模式扫描视频 / List videos using a configurable glob pattern.

    Args:
        video_dir: 视频目录。
        video_glob: 文件匹配模式，例如 `*.mp4`。
    """
    # 基于目录构造 Path 对象。
    # Build a Path object for the target directory.
    base = Path(video_dir)

    # 仅保留真正的文件，避免把目录误纳入结果。
    # Keep only files to avoid treating subdirectories as videos.
    return sorted(str(path) for path in base.glob(video_glob) if path.is_file())


def get_video_metadata(video_path: str) -> tuple[int, float, float]:
    """
    获取视频源元信息 / Get source metadata of a video.

    Returns:
        `(total_frames, fps, duration_sec)`
    """
    # 打开视频文件，读取帧数和 FPS。
    # Open the video file and read frame count plus FPS metadata.
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    # 总帧数用于后续统计汇总。
    # Total frame count is later used in batch summary statistics.
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT) or 0)

    # 原始 FPS 用于时长估计。
    # Source FPS is used to estimate video duration.
    fps = float(cap.get(cv.CAP_PROP_FPS) or 0.0)

    # 读取完元信息后及时释放资源。
    # Release resources as soon as metadata is collected.
    cap.release()

    # 若 FPS 有效，则用帧数 / FPS 计算时长，否则回退为 0。
    # Compute duration from frame count and FPS when possible.
    duration_sec = (total_frames / fps) if fps > 0 else 0.0
    return total_frames, fps, duration_sec
