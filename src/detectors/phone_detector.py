"""
手机 detector 占位实现 / Placeholder implementation for phone detection.

未来这里将接入 YOLO 系列检测器；
当前仅输出空框列表，用于打通科研原型主链路。

This file will later host a YOLO-based phone detector.
For now it emits an empty box list so the research prototype remains runnable.
"""

from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class PhoneDetector(BaseDetector):
    """手机检测占位类 / Placeholder class for phone detection."""

    # detector 稳定名称。
    # Stable detector name.
    name = "phone"

    def setup(self) -> None:
        """初始化手机 detector / Initialize the phone detector."""
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """执行单帧手机检测 / Run phone detection on a single frame."""
        # 记录开始时间，用于统计时延。
        # Record start time for latency measurement.
        t0 = perf_counter()

        # 占位实现返回空框列表，表示未检测到手机。
        # Placeholder implementation returns an empty box list.
        boxes = []

        # 只要存在任意检测框，就视作该帧出现手机。
        # Treat the frame as containing a phone if any box exists.
        phone_present = len(boxes) > 0

        # 计算推理耗时。
        # Compute inference latency.
        latency_ms = (perf_counter() - t0) * 1000.0

        # 返回统一 detector 输出。
        # Return the normalized detector output.
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"boxes": boxes, "phone_present": phone_present},
        )

    def teardown(self) -> None:
        """释放手机 detector 资源 / Release phone detector resources."""
        return
