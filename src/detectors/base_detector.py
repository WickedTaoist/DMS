from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from src.schemas.common import DetectorOutput


@dataclass(slots=True)
class FrameContext:
    """A read-only frame container passed to detectors."""

    video_id: str
    frame_index: int
    timestamp_ms: int
    frame_bgr: Any


class BaseDetector(ABC):
    """Unified detector interface for plugin-based extension."""

    name: str

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def setup(self) -> None:
        """Load model resources and runtime dependencies."""

    @abstractmethod
    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """Run per-frame inference and return a unified output."""

    @abstractmethod
    def teardown(self) -> None:
        """Release runtime resources."""
