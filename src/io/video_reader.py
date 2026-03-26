from pathlib import Path
from typing import Iterator

import cv2 as cv
import numpy as np
from numpy.typing import NDArray


def iter_video_frames(video_path: str) -> Iterator[tuple[int, NDArray[np.uint8], float]]:
    """Yield decoded frames as (frame_index, frame_bgr, source_fps)."""
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")
    fps = cap.get(cv.CAP_PROP_FPS) or 30.0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        # Keep raw BGR frame as ndarray to match OpenCV conventions.
        yield idx, frame, float(fps)
        idx += 1
    cap.release()


def list_videos(video_dir: str) -> list[str]:
    """List common video files in a directory (non-recursive)."""
    exts = {".mp4", ".avi", ".mov", ".mkv"}
    paths = []
    for path in Path(video_dir).glob("*"):
        if path.suffix.lower() in exts:
            paths.append(str(path))
    return sorted(paths)


def list_videos_by_glob(video_dir: str, video_glob: str) -> list[str]:
    """List video files using a configurable glob pattern."""
    base = Path(video_dir)
    return sorted(str(path) for path in base.glob(video_glob) if path.is_file())


def get_video_metadata(video_path: str) -> tuple[int, float, float]:
    """
    Return source metadata as (total_frames, fps, duration_sec).

    Duration falls back to 0.0 if FPS metadata is missing.
    """
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT) or 0)
    fps = float(cap.get(cv.CAP_PROP_FPS) or 0.0)
    cap.release()
    duration_sec = (total_frames / fps) if fps > 0 else 0.0
    return total_frames, fps, duration_sec
