"""
融合器抽象接口模块 / Base interface for fusion strategies.

融合器负责把多个 detector 的输出转换为统一证据表示和风险分数，
使后续判定层不需要关心每个 detector 的细节。

Fusers transform multiple detector outputs into unified evidence
representations and risk scores, so later decision layers do not need
to know detector-specific details.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFuser(ABC):
    """
    证据融合抽象基类 / Abstract base class for evidence fusion.

    所有融合策略都应继承本类，并实现 `fuse()` 方法。
    Every concrete fusion strategy should inherit from this class and
    implement `fuse()`.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        # 保存融合配置，例如权重参数。
        # Store fusion config, such as evidence weights.
        self.config = config

    @abstractmethod
    def fuse(self, detector_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        将 detector 输出融合为证据分数和风险分数 / Fuse detector outputs.

        Args:
            detector_outputs: 按 detector 名字组织的输出结果。

        Returns:
            包含 evidence scores 和 risk score 的字典。
            A dictionary containing evidence scores and a risk score.
        """
