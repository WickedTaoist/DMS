from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class ClipSummary:
    """Top-level summary for a whole processed clip."""

    video_id: str
    total_frames_processed: int
    fps_processed: float
    total_duration_ms: int
    event_count_phone_usage: int
    event_total_duration_ms: int
    event_duration_ratio: float
    max_event_duration_ms: int
    avg_event_duration_ms: float
    clip_label: str
    clip_risk_score: float
    model_versions: Dict[str, str] = field(default_factory=dict)
