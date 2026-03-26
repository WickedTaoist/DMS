from time import perf_counter

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class GazeDetector(BaseDetector):
    """Placeholder gaze detector for prototype integration."""

    name = "gaze"

    def setup(self) -> None:
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        t0 = perf_counter()
        gaze_pitch = 0.0
        is_gaze_down = gaze_pitch >= float(self.config.get("gaze_down_threshold", 10.0))
        latency_ms = (perf_counter() - t0) * 1000.0
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=latency_ms,
            confidence=0.5,
            payload={"gaze_pitch": gaze_pitch, "is_gaze_down": is_gaze_down},
        )

    def teardown(self) -> None:
        return
