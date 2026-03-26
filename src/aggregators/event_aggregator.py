from typing import List

from src.schemas.event_result import EventResult
from src.schemas.frame_result import FrameResult
from src.utils.id_utils import make_event_id


def aggregate_events(
    frame_results: List[FrameResult], min_event_frames: int, target_label: str = "phone_usage_suspected"
) -> List[EventResult]:
    """Convert frame-level labels into continuous event segments."""
    events: List[EventResult] = []
    start_idx = None

    for i, fr in enumerate(frame_results):
        label = fr.decision.get("frame_label", "normal")
        if label == target_label and start_idx is None:
            start_idx = i
        if label != target_label and start_idx is not None:
            _flush_event(frame_results, start_idx, i - 1, min_event_frames, events)
            start_idx = None

    if start_idx is not None:
        _flush_event(frame_results, start_idx, len(frame_results) - 1, min_event_frames, events)
    return events


def _flush_event(
    frame_results: List[FrameResult],
    start_idx: int,
    end_idx: int,
    min_event_frames: int,
    out_events: List[EventResult],
) -> None:
    length = end_idx - start_idx + 1
    if length < min_event_frames:
        return

    chunk = frame_results[start_idx : end_idx + 1]
    scores = [float(x.fusion.get("risk_score", 0.0)) for x in chunk]
    video_id = chunk[0].meta.video_id
    start_ms = chunk[0].meta.timestamp_ms
    end_ms = chunk[-1].meta.timestamp_ms
    out_events.append(
        EventResult(
            event_id=make_event_id(video_id, start_idx, end_idx),
            video_id=video_id,
            event_type="phone_usage",
            start_frame=chunk[0].meta.frame_index,
            end_frame=chunk[-1].meta.frame_index,
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=max(0, end_ms - start_ms),
            peak_risk_score=max(scores) if scores else 0.0,
            mean_risk_score=(sum(scores) / len(scores)) if scores else 0.0,
            evidence_stats={},
            decision_reason="rule_based_temporal_aggregation",
        )
    )
