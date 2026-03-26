from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput


class VLMDetector(BaseDetector):
    """Reserved interface for future VLM semantic detector."""

    name = "vlm"

    def setup(self) -> None:
        return

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        return DetectorOutput(
            detector_name=self.name,
            success=True,
            latency_ms=0.0,
            confidence=None,
            payload={"vlm_reasoning": "", "vlm_score": 0.0},
        )

    def teardown(self) -> None:
        return
