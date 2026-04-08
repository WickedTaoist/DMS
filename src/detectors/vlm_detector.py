"""
VLM detector 预留接口 / Reserved interface for future VLM detector.

该模块为未来接入 Vision-Language Model 预留位置，
当前只返回空推理结果，确保整体系统结构提前稳定。

This module reserves a future integration point for a Vision-Language Model.
It currently returns an empty inference result so the overall system
architecture can be stabilized early.
"""

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class VLMDetector(BaseDetector):
    """VLM detector 预留类 / Reserved class for a future VLM detector."""

    # detector 稳定名称。
    # Stable detector name.
    name = "vlm"

    def setup(self) -> None:
        """初始化 VLM detector / Initialize the VLM detector."""
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """
        执行 VLM 推理占位逻辑 / Run placeholder VLM inference logic.

        当前仅返回空推理文本和 0 分数。
        The current implementation only returns empty reasoning text and a zero score.
        """
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=0.0,
            confidence=None,
            payload={"vlm_reasoning": "", "vlm_score": 0.0},
        )

    def teardown(self) -> None:
        """释放 VLM detector 资源 / Release VLM detector resources."""
        return
