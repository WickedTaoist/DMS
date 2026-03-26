from dataclasses import dataclass, field
from typing import Any, Dict

from src.schemas.common import FrameMeta


@dataclass(slots=True)
class FrameResult:
    """Stores all detector evidence and decision for one frame."""

    meta: FrameMeta
    detector_outputs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    fusion: Dict[str, Any] = field(default_factory=dict)
    decision: Dict[str, Any] = field(default_factory=dict)
