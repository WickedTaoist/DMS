from dataclasses import dataclass


@dataclass(slots=True)
class ThresholdPolicy:
    """Collects configurable thresholds for decision logic."""

    frame_risk_threshold: float = 0.6
    min_event_frames: int = 8
    max_gap_frames: int = 3
