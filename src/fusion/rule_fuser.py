"""
规则融合模块 / Rule-based fusion strategy.

该模块提供一个可解释的 baseline 融合器：
把多个 detector 的布尔/弱分数信号按权重加和，得到统一 `risk_score`。

This module provides an interpretable baseline fuser:
it combines multiple detector signals with weighted summation
to produce a unified `risk_score`.
"""

from typing import Any, Dict

from src.fusion.base_fuser import BaseFuser


class RuleFuser(BaseFuser):
    """
    基于规则的证据融合器 / Rule-based evidence fuser.

    该实现追求：
    1. 简单
    2. 可解释
    3. 便于做论文初期 baseline 与消融实验

    This implementation aims to be:
    1. Simple
    2. Interpretable
    3. Suitable for early baselines and ablation studies
    """

    def fuse(self, detector_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        融合 detector 输出 / Fuse detector outputs into evidence and risk score.

        Args:
            detector_outputs: 来自 `FramePipeline` 的 detector 输出字典。

        Returns:
            包含 `evidence_scores` 和 `risk_score` 的字典。
            A dictionary containing `evidence_scores` and `risk_score`.
        """
        # 从配置中读取权重；若未提供，则使用默认值。
        # Read evidence weights from config, falling back to defaults.
        weights = self.config.get("weights", {})

        # 每个 detector 在 `FramePipeline` 中都以统一 envelope 包装，
        # 真正业务字段存放在 `payload` 下。
        #
        # Each detector output is wrapped in a normalized envelope inside
        # `FramePipeline`, and the actual detector-specific fields live under `payload`.
        head_payload = detector_outputs.get("head_pose", {}).get("payload", {})
        gaze_payload = detector_outputs.get("gaze", {}).get("payload", {})
        phone_payload = detector_outputs.get("phone", {}).get("payload", {})
        hand_payload = detector_outputs.get("hand_off_wheel", {}).get("payload", {})

        # 将 detector 的布尔信号映射为 0/1 分数，作为 baseline 证据输入。
        # Convert detector booleans into 0/1 scores as baseline evidence values.
        head_down_score = float(bool(head_payload.get("is_head_down", False)))
        gaze_down_score = float(bool(gaze_payload.get("is_gaze_down", False)))
        phone_score = float(bool(phone_payload.get("phone_present", False)))
        hand_off_score = float(bool(hand_payload.get("hand_off", False)))

        # 使用加权和计算统一风险分数。
        # Use weighted summation to compute a unified risk score.
        risk = (
            head_down_score * float(weights.get("head_down", 0.25))
            + gaze_down_score * float(weights.get("gaze_down", 0.25))
            + phone_score * float(weights.get("phone_present", 0.35))
            + hand_off_score * float(weights.get("hand_off", 0.15))
        )

        # 返回结构化融合结果，便于后续判定层和导出层统一处理。
        # Return structured fusion output for decision and exporting.
        return {
            "evidence_scores": {
                "head_down_score": head_down_score,
                "gaze_down_score": gaze_down_score,
                "phone_score": phone_score,
                "hand_off_score": hand_off_score,
            },
            "risk_score": float(risk),
        }
