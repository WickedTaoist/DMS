from typing import Any, Dict

from src.io.video_reader import list_videos
from src.runners.run_single import run_single


def run_batch(video_dir: str, config: Dict[str, Any], logger) -> None:
    videos = list_videos(video_dir)
    logger.info("Discovered %s videos under %s", len(videos), video_dir)
    for path in videos:
        run_single(path, config, logger)
