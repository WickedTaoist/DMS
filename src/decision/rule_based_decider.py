from typing import Any, Dict

from src.decision.base_decider import BaseDecider


class RuleBasedDecider(BaseDecider):
    """Baseline threshold decision from fused risk score."""

    def decide(self, fusion_output: Dict[str, Any]) -> Dict[str, Any]:
        risk = float(fusion_output.get("risk_score", 0.0))
        threshold = float(self.config.get("frame_risk_threshold", 0.6))
        label = "suspected_phone_use" if risk >= threshold else "normal"
        return {"frame_label": label, "decision_confidence": risk}
