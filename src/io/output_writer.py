import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from src.schemas.clip_summary import ClipSummary
from src.schemas.event_result import EventResult
from src.schemas.frame_result import FrameResult


def write_json_outputs(
    output_dir: str,
    stem: str,
    frame_results: List[FrameResult],
    event_results: List[EventResult],
    clip_summary: ClipSummary,
) -> dict[str, str]:
    json_dir = Path(output_dir) / "json" / stem
    json_dir.mkdir(parents=True, exist_ok=True)
    with (json_dir / "frame_results.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in frame_results], f, ensure_ascii=False, indent=2)
    with (json_dir / "events.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in event_results], f, ensure_ascii=False, indent=2)
    with (json_dir / "clip_summary.json").open("w", encoding="utf-8") as f:
        json.dump(asdict(clip_summary), f, ensure_ascii=False, indent=2)
    return {
        "frame_json_path": str((json_dir / "frame_results.json").resolve()),
        "events_json_path": str((json_dir / "events.json").resolve()),
        "clip_json_path": str((json_dir / "clip_summary.json").resolve()),
    }


def write_csv_outputs(
    output_dir: str,
    stem: str,
    frame_results: List[FrameResult],
    event_results: List[EventResult],
    clip_summary: ClipSummary,
) -> dict[str, str]:
    csv_dir = Path(output_dir) / "csv" / stem
    csv_dir.mkdir(parents=True, exist_ok=True)

    with (csv_dir / "frame_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["video_id", "frame_index", "timestamp_ms", "frame_label", "risk_score"],
        )
        writer.writeheader()
        for fr in frame_results:
            writer.writerow(
                {
                    "video_id": fr.meta.video_id,
                    "frame_index": fr.meta.frame_index,
                    "timestamp_ms": fr.meta.timestamp_ms,
                    "frame_label": fr.decision.get("frame_label", "normal"),
                    "risk_score": fr.fusion.get("risk_score", 0.0),
                }
            )

    with (csv_dir / "events.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "event_id",
                "video_id",
                "event_type",
                "start_frame",
                "end_frame",
                "duration_frames",
                "duration_ms",
                "max_risk_score",
                "mean_risk_score",
            ],
        )
        writer.writeheader()
        for ev in event_results:
            writer.writerow(
                {
                    "event_id": ev.event_id,
                    "video_id": ev.video_id,
                    "event_type": ev.event_type,
                    "start_frame": ev.start_frame,
                    "end_frame": ev.end_frame,
                    "duration_frames": ev.duration_frames,
                    "duration_ms": ev.duration_ms,
                    "max_risk_score": ev.max_risk_score,
                    "mean_risk_score": ev.mean_risk_score,
                }
            )

    with (csv_dir / "clip_summary.csv").open("w", newline="", encoding="utf-8") as f:
        clip = asdict(clip_summary)
        writer = csv.DictWriter(f, fieldnames=list(clip.keys()))
        writer.writeheader()
        writer.writerow(clip)
    return {
        "frame_csv_path": str((csv_dir / "frame_results.csv").resolve()),
        "events_csv_path": str((csv_dir / "events.csv").resolve()),
        "clip_csv_path": str((csv_dir / "clip_summary.csv").resolve()),
    }
