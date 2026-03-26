from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class HandOffWheelDetector(BaseDetector):
    """Placeholder hand-off-wheel detector for future integration."""

    name = "hand_off_wheel"

    def setup(self) -> None:
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        t0 = perf_counter()
        hand_off = False
        latency_ms = (perf_counter() - t0) * 1000.0
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"hand_off": hand_off},
        )

    def teardown(self) -> None:
        return
