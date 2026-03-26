import csv
import logging
from typing import Any, Dict

from src.io.video_reader import list_videos_by_glob
from src.runners.run_single import SingleRunResult, run_single
from src.utils.path_utils import ensure_directory_exists, resolve_project_path
from src.utils.video_name_parser import VideoNameParser


def run_batch(config: Dict[str, Any], logger: logging.Logger, input_dir_override: str | None = None) -> None:
    """
    Run batch pipeline on all videos discovered from config.

    The runner is intentionally resilient: a single corrupt/invalid video does
    not terminate the full experiment. Failed files are logged and skipped.
    """
    data_cfg = config.get("data", {})
    video_dir_cfg = input_dir_override or data_cfg.get("video_dir", "data/video")
    video_glob = data_cfg.get("video_glob", "*.mp4")

    video_dir = resolve_project_path(video_dir_cfg)
    ensure_directory_exists(video_dir, "Configured video_dir")
    logger.info("Resolved video_dir: %s", video_dir)
    logger.info("Using video_glob: %s", video_glob)

    videos = list_videos_by_glob(str(video_dir), video_glob)
    logger.info("Discovered %s videos for batch run", len(videos))
    if not videos:
        logger.warning("No videos matched pattern: %s", video_glob)
        return

    parser = VideoNameParser()
    rows: list[dict[str, Any]] = []
    total = len(videos)
    for idx, path in enumerate(videos, start=1):
        logger.info("Progress %s/%s | Processing: %s", idx, total, path)
        info = parser.parse(path)
        try:
            result: SingleRunResult = run_single(path, config, logger)
            row = {
                "video_id": info.video_id,
                "file_name": info.file_name,
                "file_path": result.video_path,
                "parsed_label": info.parsed_label,
                "total_frames": result.total_frames,
                "processed_frames": result.processed_frames,
                "duration_sec": round(result.duration_sec, 4),
                "num_events": result.num_events,
                "total_event_duration_sec": round(result.total_event_duration_sec, 4),
                "max_risk_score": round(result.max_risk_score, 6),
                "clip_label": result.clip_label,
                "output_json_path": result.output_json_path,
                "output_csv_path": result.output_csv_path,
                "status": "ok",
                "error_message": "",
            }
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed video: %s", path)
            row = {
                "video_id": info.video_id,
                "file_name": info.file_name,
                "file_path": str(resolve_project_path(path)),
                "parsed_label": info.parsed_label,
                "total_frames": 0,
                "processed_frames": 0,
                "duration_sec": 0.0,
                "num_events": 0,
                "total_event_duration_sec": 0.0,
                "max_risk_score": 0.0,
                "clip_label": "failed",
                "output_json_path": "",
                "output_csv_path": "",
                "status": "failed",
                "error_message": str(exc),
            }
        rows.append(row)

    _write_batch_summary(config, rows)


def _write_batch_summary(config: Dict[str, Any], rows: list[dict[str, Any]]) -> None:
    """Write cross-video batch summary table for experiment analysis."""
    output_root = resolve_project_path(config.get("output", {}).get("root_dir", "outputs"))
    csv_root = output_root / "csv"
    csv_root.mkdir(parents=True, exist_ok=True)
    summary_path = csv_root / "batch_summary.csv"

    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with summary_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
