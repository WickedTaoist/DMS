from pathlib import Path
from typing import Any, Dict

from src.decision.rule_based_decider import RuleBasedDecider
from src.detectors.registry import build_detectors
from src.fusion.rule_fuser import RuleFuser
from src.io.output_writer import write_csv_outputs, write_json_outputs
from src.pipelines.clip_pipeline import ClipPipeline
from src.pipelines.frame_pipeline import FramePipeline


def run_single(video_path: str, config: Dict[str, Any], logger) -> None:
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
        frame_results, event_results, clip_summary = clip_pipeline.run(video_path)

        output_dir = config["project"].get("output_dir", "outputs")
        stem = Path(video_path).stem
        if config["runtime"].get("save_json", True):
            write_json_outputs(output_dir, stem, frame_results, event_results, clip_summary)
        if config["runtime"].get("save_csv", True):
            write_csv_outputs(output_dir, stem, frame_results, event_results, clip_summary)
        logger.info("Finished video: %s | frames=%s | events=%s", video_path, len(frame_results), len(event_results))
    finally:
        for d in detectors:
            d.teardown()
