from typing import Any, Dict

from src.fusion.base_fuser import BaseFuser


class RuleFuser(BaseFuser):
    """Simple weighted fusion for interpretable baseline experiments."""

    def fuse(self, detector_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        weights = self.config.get("weights", {})
        # Detector payload is nested under each detector envelope.
        head_payload = detector_outputs.get("head_pose", {}).get("payload", {})
        gaze_payload = detector_outputs.get("gaze", {}).get("payload", {})
        phone_payload = detector_outputs.get("phone", {}).get("payload", {})
        hand_payload = detector_outputs.get("hand_off_wheel", {}).get("payload", {})

        head_down_score = float(bool(head_payload.get("is_head_down", False)))
        gaze_down_score = float(bool(gaze_payload.get("is_gaze_down", False)))
        phone_score = float(bool(phone_payload.get("phone_present", False)))
        hand_off_score = float(bool(hand_payload.get("hand_off", False)))
        risk = (
            head_down_score * float(weights.get("head_down", 0.25))
            + gaze_down_score * float(weights.get("gaze_down", 0.25))
            + phone_score * float(weights.get("phone_present", 0.35))
            + hand_off_score * float(weights.get("hand_off", 0.15))
        )
        return {
            "evidence_scores": {
                "head_down_score": head_down_score,
                "gaze_down_score": gaze_down_score,
                "phone_score": phone_score,
                "hand_off_score": hand_off_score,
            },
            "risk_score": float(risk),
        }
