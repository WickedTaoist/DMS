"""
判定器抽象接口模块 / Base interface for decider implementations.

判定器负责把融合结果转换成任务标签，
例如把 `risk_score` 转换成 `normal` 或 `suspected_phone_use`。

Deciders convert fusion outputs into task-specific labels,
for example turning a `risk_score` into `normal` or `suspected_phone_use`.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseDecider(ABC):
    """
    帧级行为判定抽象基类 / Abstract base class for frame-level decisions.

    所有具体判定器都应继承本类，并实现 `decide()` 方法。
    Every concrete decider should inherit from this class and implement `decide()`.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        # 保存判定器配置，供子类在阈值或规则中使用。
        # Store decider config for thresholds and rule logic in subclasses.
        self.config = config

    @abstractmethod
    def decide(self, fusion_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据融合结果生成判定输出 / Produce a decision payload from fusion output.

        Args:
            fusion_output: 融合模块产出的结构化结果。

        Returns:
            帧级判定字典，例如标签和置信度。
            A frame-level decision dictionary such as label and confidence.
        """
