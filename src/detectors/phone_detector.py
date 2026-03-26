from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class PhoneDetector(BaseDetector):
    """Placeholder phone detector for YOLO integration."""

    name = "phone"

    def setup(self) -> None:
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        t0 = perf_counter()
        boxes = []
        phone_present = len(boxes) > 0
        latency_ms = (perf_counter() - t0) * 1000.0
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"boxes": boxes, "phone_present": phone_present},
        )

    def teardown(self) -> None:
        return
