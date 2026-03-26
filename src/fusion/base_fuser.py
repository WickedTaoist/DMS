from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFuser(ABC):
    """Unified interface for evidence fusion strategies."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def fuse(self, detector_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Combine detector outputs into evidence scores and risk score."""
