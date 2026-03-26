from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(slots=True)
class FrameMeta:
    """Metadata describing a single decoded frame."""

    video_id: str
    frame_index: int
    timestamp_ms: int


@dataclass(slots=True)
class BBox:
    """Bounding box in xyxy format."""

    x1: float
    y1: float
    x2: float
    y2: float
    score: float
    label: str


@dataclass(slots=True)
class DetectorOutput:
    """Unified output envelope for all detectors."""

    detector_name: str
    success: bool
    latency_ms: float
    confidence: Optional[float]
    payload: Dict[str, Any]
    error: Optional[str] = None
