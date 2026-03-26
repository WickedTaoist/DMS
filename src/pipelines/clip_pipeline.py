from pathlib import Path
from typing import Dict, List, Tuple

from src.aggregators.event_aggregator import aggregate_events
from src.aggregators.temporal_smoother import smooth_labels
from src.detectors.base_detector import FrameContext
from src.io.frame_sampler import should_keep_frame
from src.io.video_reader import iter_video_frames
from src.pipelines.frame_pipeline import FramePipeline
from src.schemas.clip_summary import ClipSummary
from src.schemas.event_result import EventResult
from src.schemas.frame_result import FrameResult
from src.utils.time_utils import frame_to_timestamp_ms


class ClipPipeline:
    """Orchestrates the full per-video processing flow."""

    def __init__(self, frame_pipeline: FramePipeline, config: Dict) -> None:
        self.frame_pipeline = frame_pipeline
        self.config = config

    def run(self, video_path: str) -> Tuple[List[FrameResult], List[EventResult], ClipSummary]:
        video_id = Path(video_path).name
        target_fps = float(self.config["runtime"].get("sample_fps", 10))
        frame_results: List[FrameResult] = []
        src_fps = 30.0

        for frame_index, frame_bgr, src_fps in iter_video_frames(video_path):
            if not should_keep_frame(frame_index, src_fps, target_fps):
                continue
            frame_ctx = FrameContext(
                video_id=video_id,
                frame_index=frame_index,
                timestamp_ms=frame_to_timestamp_ms(frame_index, src_fps),
                frame_bgr=frame_bgr,
            )
            frame_results.append(self.frame_pipeline.process(frame_ctx))

        labels = [fr.decision.get("frame_label", "normal") for fr in frame_results]
        smoothed = smooth_labels(labels, int(self.config["decision"].get("max_gap_frames", 3)))
        for fr, label in zip(frame_results, smoothed):
            fr.decision["frame_label"] = label

        events = aggregate_events(
            frame_results=frame_results,
            min_event_frames=int(self.config["decision"].get("min_event_frames", 8)),
        )
        summary = self._build_summary(video_id, frame_results, events, target_fps)
        return frame_results, events, summary

    @staticmethod
    def _build_summary(
        video_id: str, frame_results: List[FrameResult], events: List[EventResult], fps_processed: float
    ) -> ClipSummary:
        total_frames = len(frame_results)
        total_duration_ms = frame_results[-1].meta.timestamp_ms if frame_results else 0
        event_duration_ms = sum(ev.duration_ms for ev in events)
        event_count = len(events)
        max_event_duration = max((ev.duration_ms for ev in events), default=0)
        avg_event_duration = (event_duration_ms / event_count) if event_count else 0.0
        clip_risk = max((float(fr.fusion.get("risk_score", 0.0)) for fr in frame_results), default=0.0)
        clip_label = "phone_usage_present" if event_count > 0 else "normal"
        ratio = (event_duration_ms / total_duration_ms) if total_duration_ms > 0 else 0.0
        return ClipSummary(
            video_id=video_id,
            total_frames_processed=total_frames,
            fps_processed=fps_processed,
            total_duration_ms=total_duration_ms,
            event_count_phone_usage=event_count,
            event_total_duration_ms=event_duration_ms,
            event_duration_ratio=ratio,
            max_event_duration_ms=max_event_duration,
            avg_event_duration_ms=avg_event_duration,
            clip_label=clip_label,
            clip_risk_score=clip_risk,
            model_versions={},
        )
