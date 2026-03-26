from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class HeadPoseDetector(BaseDetector):
    """Placeholder head pose detector for prototype integration."""

    name = "head_pose"

    def setup(self) -> None:
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        t0 = perf_counter()
        pitch = 0.0
        is_head_down = pitch >= float(self.config.get("pitch_down_threshold", 15.0))
        latency_ms = (perf_counter() - t0) * 1000.0
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"pitch": pitch, "is_head_down": is_head_down},
        )

    def teardown(self) -> None:
        return
