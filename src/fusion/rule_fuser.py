from typing import Any, Dict

from src.fusion.base_fuser import BaseFuser


class RuleFuser(BaseFuser):
    """Simple weighted fusion for interpretable baseline experiments."""

    def fuse(self, detector_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        weights = self.config.get("weights", {})
        head_down = float(detector_outputs.get("head_pose", {}).get("is_head_down", 0))
        gaze_down = float(detector_outputs.get("gaze", {}).get("is_gaze_down", 0))
        phone_present = float(detector_outputs.get("phone", {}).get("phone_present", 0))
        hand_off = float(detector_outputs.get("hand_off_wheel", {}).get("hand_off", 0))
        risk = (
            head_down * float(weights.get("head_down", 0.25))
            + gaze_down * float(weights.get("gaze_down", 0.25))
            + phone_present * float(weights.get("phone_present", 0.35))
            + hand_off * float(weights.get("hand_off", 0.15))
        )
        return {
            "evidence_scores": {
                "head_down": head_down,
                "gaze_down": gaze_down,
                "phone_present": phone_present,
                "hand_off": hand_off,
            },
            "risk_score": float(risk),
        }
