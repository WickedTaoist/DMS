"""
视线 detector 占位实现 / Placeholder implementation for gaze detection.

当前版本不接入真实 gaze estimation 模型，
只输出固定值用于验证系统主流程。

The current version does not integrate a real gaze estimation model.
It emits fixed values so the main system pipeline can be validated.
"""

from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class GazeDetector(BaseDetector):
    """视线 detector 占位类 / Placeholder class for gaze detection."""

    # 配置和输出中使用的 detector 名称。
    # Detector name used in config and outputs.
    name = "gaze"

    def setup(self) -> None:
        """初始化视线 detector / Initialize the gaze detector."""
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """执行单帧视线推理 / Run gaze inference on a single frame."""
        # 开始计时，估计本次 detector 延迟。
        # Start timing to estimate detector latency.
        t0 = perf_counter()

        # 占位实现固定 gaze pitch。
        # Placeholder implementation uses a fixed gaze pitch.
        gaze_pitch = 0.0

        # 将 gaze pitch 与阈值比较得到 `is_gaze_down`。
        # Compare gaze pitch against threshold to derive `is_gaze_down`.
        is_gaze_down = gaze_pitch >= float(self.config.get("gaze_down_threshold", 10.0))

        # 计算耗时（毫秒）。
        # Compute latency in milliseconds.
        latency_ms = (perf_counter() - t0) * 1000.0

        # 返回统一 detector 输出结构。
        # Return the normalized detector output structure.
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"gaze_pitch": gaze_pitch, "is_gaze_down": is_gaze_down},
        )

    def teardown(self) -> None:
        """释放视线 detector 资源 / Release gaze detector resources."""
        return
