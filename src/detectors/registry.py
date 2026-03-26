from typing import Any, Dict, List

from src.detectors.base_detector import BaseDetector
from src.detectors.gaze_detector import GazeDetector
from src.detectors.hand_off_wheel_detector import HandOffWheelDetector
from src.detectors.head_pose_detector import HeadPoseDetector
from src.detectors.phone_detector import PhoneDetector
from src.detectors.vlm_detector import VLMDetector


DETECTOR_REGISTRY = {
    "head_pose": HeadPoseDetector,
    "gaze": GazeDetector,
    "phone": PhoneDetector,
    "hand_off_wheel": HandOffWheelDetector,
    "vlm": VLMDetector,
}


def build_detectors(config: Dict[str, Any]) -> List[BaseDetector]:
    """Create detector instances based on config entries."""
    enabled = config["detectors"]["enabled"]
    detector_cfg = config["detectors"]["configs"]
    detectors: List[BaseDetector] = []
    for name in enabled:
        if name not in DETECTOR_REGISTRY:
            raise ValueError(f"Unknown detector: {name}")
        cls = DETECTOR_REGISTRY[name]
        detectors.append(cls(detector_cfg.get(name, {})))
    return detectors
