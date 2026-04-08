"""
规则判定模块 / Rule-based decision strategy.

该模块把融合模块输出的 `risk_score` 转换为最终帧级标签，
是当前科研原型中最基础、最可解释的判定方式。

This module converts the `risk_score` produced by the fuser
into the final frame-level label. It is the simplest and most
interpretable decision strategy in the current prototype.
"""

from typing import Any, Dict

from src.decision.base_decider import BaseDecider


class RuleBasedDecider(BaseDecider):
    """规则判定器 / Rule-based decider."""

    def decide(self, fusion_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据风险分数生成帧级标签 / Generate a frame label from the risk score.

        Args:
            fusion_output: 融合模块输出。

        Returns:
            包含 `frame_label` 和 `decision_confidence` 的字典。
            A dictionary containing `frame_label` and `decision_confidence`.
        """
        # 从融合结果中读取风险分数。
        # Read the risk score from fusion output.
        risk = float(fusion_output.get("risk_score", 0.0))

        # 从配置中读取帧级判定阈值。
        # Read the frame-level decision threshold from config.
        threshold = float(self.config.get("frame_risk_threshold", 0.6))

        # 风险高于阈值则标为可疑玩手机，否则为正常。
        # Mark the frame as suspicious phone use when risk exceeds the threshold.
        label = "suspected_phone_use" if risk >= threshold else "normal"

        # 当前 baseline 直接使用 risk 作为 decision_confidence。
        # The current baseline directly reuses risk as decision confidence.
        return {"frame_label": label, "decision_confidence": risk}
