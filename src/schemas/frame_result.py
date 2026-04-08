"""
帧级结果结构模块 / Frame-level result schema.

本模块定义单帧处理后的完整结果结构，
用于承载 detector 原始输出、融合结果以及最终判定结果。

This module defines the complete per-frame result structure,
including detector raw outputs, fusion results, and final decisions.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from src.schemas.common import FrameMeta


@dataclass(slots=True)
class FrameResult:
    """
    单帧完整结果 / Complete processing result for one frame.

    Attributes:
        meta: 帧级元信息。
        detector_outputs: 各 detector 的原始输出封装。
        fusion: 融合模块输出，如 evidence scores 和 risk score。
        decision: 判定模块输出，如 frame label 和 confidence。
    """

    # 帧的基本定位信息。
    # Basic identity and time metadata of the frame.
    meta: FrameMeta

    # 各 detector 输出，按 detector 名字组织。
    # Detector outputs organized by detector name.
    detector_outputs: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # 融合模块结果，例如风险分数。
    # Fusion results such as evidence scores and risk score.
    fusion: Dict[str, Any] = field(default_factory=dict)

    # 判定模块结果，例如帧标签与置信度。
    # Decision outputs such as frame label and confidence.
    decision: Dict[str, Any] = field(default_factory=dict)
