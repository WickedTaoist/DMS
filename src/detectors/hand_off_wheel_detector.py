"""
手离方向盘 detector 占位实现 / Placeholder implementation for hand-off-wheel detection.

当前仅返回固定的 `False` 信号，
后续可以替换为基于手部/方向盘区域关系的真实模型或规则。

This implementation currently returns a fixed `False` signal.
It can later be replaced by a real detector or rule based on
hands and steering-wheel interaction.
"""

from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class HandOffWheelDetector(BaseDetector):
    """手离方向盘 detector 占位类 / Placeholder hand-off-wheel detector."""

    # detector 稳定名称。
    # Stable detector name.
    name = "hand_off_wheel"

    def setup(self) -> None:
        """初始化手离方向盘 detector / Initialize the hand-off-wheel detector."""
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """执行单帧手离方向盘推理 / Run hand-off-wheel inference on one frame."""
        # 记录开始时间，便于统一统计时延。
        # Record the start time for consistent latency statistics.
        t0 = perf_counter()

        # 占位实现固定认为双手未离开方向盘。
        # Placeholder implementation assumes hands are not off the wheel.
        hand_off = False

        # 计算耗时（毫秒）。
        # Compute latency in milliseconds.
        latency_ms = (perf_counter() - t0) * 1000.0

        # 返回统一 detector 输出格式。
        # Return the normalized detector output format.
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"hand_off": hand_off},
        )

    def teardown(self) -> None:
        """释放手离方向盘 detector 资源 / Release hand-off-wheel detector resources."""
        return
