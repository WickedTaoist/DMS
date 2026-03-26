from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from src.decision.rule_based_decider import RuleBasedDecider
from src.detectors.registry import build_detectors
from src.fusion.rule_fuser import RuleFuser
from src.io.video_reader import get_video_metadata
from src.io.output_writer import write_csv_outputs, write_json_outputs
from src.pipelines.clip_pipeline import ClipPipeline
from src.pipelines.frame_pipeline import FramePipeline
from src.utils.path_utils import resolve_project_path


@dataclass(slots=True)
class SingleRunResult:
    """Structured outputs for one processed video."""

    video_path: str
    total_frames: int
    duration_sec: float
    processed_frames: int
    num_events: int
    total_event_duration_sec: float
    max_risk_score: float
    clip_label: str
    output_json_path: str
    output_csv_path: str


def run_single(video_path: str, config: Dict[str, Any], logger) -> SingleRunResult:
    """Run complete clip pipeline on one video and return summary metadata."""
    abs_video_path = str(resolve_project_path(video_path))
    detectors = build_detectors(config)
    for d in detectors:
        d.setup()
    try:
        frame_pipeline = FramePipeline(
            detectors=detectors,
            fuser=RuleFuser(config.get("fusion", {})),
            decider=RuleBasedDecider(config.get("decision", {})),
        )
        clip_pipeline = ClipPipeline(frame_pipeline=frame_pipeline, config=config)
        frame_results, event_results, clip_summary = clip_pipeline.run(abs_video_path)

        output_root = config.get("output", {}).get("root_dir", "outputs")
        output_dir = str(resolve_project_path(output_root))
        stem = Path(abs_video_path).stem
        json_paths = {}
        csv_paths = {}
        if config["runtime"].get("save_json", True):
            json_paths = write_json_outputs(output_dir, stem, frame_results, event_results, clip_summary)
        if config["runtime"].get("save_csv", True):
            csv_paths = write_csv_outputs(output_dir, stem, frame_results, event_results, clip_summary)

        total_frames, _src_fps, duration_sec = get_video_metadata(abs_video_path)
        total_event_duration_sec = clip_summary.event_total_duration_ms / 1000.0
        logger.info(
            "Finished video: %s | processed_frames=%s | events=%s",
            abs_video_path,
            len(frame_results),
            len(event_results),
        )
        return SingleRunResult(
            video_path=abs_video_path,
            total_frames=total_frames,
            duration_sec=duration_sec,
            processed_frames=len(frame_results),
            num_events=len(event_results),
            total_event_duration_sec=total_event_duration_sec,
            max_risk_score=float(clip_summary.clip_risk_score),
            clip_label=clip_summary.clip_label,
            output_json_path=json_paths.get("clip_json_path", ""),
            output_csv_path=csv_paths.get("frame_csv_path", ""),
        )
    finally:
        for d in detectors:
            d.teardown()
