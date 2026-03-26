from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseDecider(ABC):
    """Unified interface for frame-level behavior decision."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def decide(self, fusion_output: Dict[str, Any]) -> Dict[str, Any]:
        """Return a frame-level decision payload."""
