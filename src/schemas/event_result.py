from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class EventResult:
    """Represents one continuous behavior event segment."""

    event_id: str
    video_id: str
    event_type: str
    start_frame: int
    end_frame: int
    start_ms: int
    end_ms: int
    duration_ms: int
    peak_risk_score: float
    mean_risk_score: float
    evidence_stats: Dict[str, float] = field(default_factory=dict)
    decision_reason: str = ""
