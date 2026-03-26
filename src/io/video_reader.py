from pathlib import Path
from typing import Iterator, Tuple

import cv2 as cv


def iter_video_frames(video_path: str) -> Iterator[Tuple[int, any, float]]:
    """Yield (frame_index, frame_bgr, source_fps) from a video."""
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")
    fps = cap.get(cv.CAP_PROP_FPS) or 30.0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        yield idx, frame, float(fps)
        idx += 1
    cap.release()


def list_videos(video_dir: str) -> list[str]:
    exts = {".mp4", ".avi", ".mov", ".mkv"}
    paths = []
    for path in Path(video_dir).glob("*"):
        if path.suffix.lower() in exts:
            paths.append(str(path))
    return sorted(paths)
