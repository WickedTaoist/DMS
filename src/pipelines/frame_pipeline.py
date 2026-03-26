from src.decision.base_decider import BaseDecider
from src.detectors.base_detector import BaseDetector, FrameContext
from src.fusion.base_fuser import BaseFuser
from src.schemas.common import FrameMeta
from src.schemas.frame_result import FrameResult


class FramePipeline:
    """Per-frame processing: detect -> fuse -> decide."""

    def __init__(self, detectors: list[BaseDetector], fuser: BaseFuser, decider: BaseDecider) -> None:
        self.detectors = detectors
        self.fuser = fuser
        self.decider = decider

    def process(self, frame_ctx: FrameContext) -> FrameResult:
        # Raw detector results are preserved for later ablation and error analysis.
        detector_outputs: dict[str, dict] = {}
        for detector in self.detectors:
            out = detector.infer(frame_ctx)
            detector_outputs[detector.name] = {
                "success": out.success,
                "latency_ms": out.latency_ms,
                "confidence": out.confidence,
                "payload": out.payload,
                "error": out.error,
            }

        # Fuser consumes normalized detector outputs and produces evidence + risk.
        fusion_output = self.fuser.fuse(detector_outputs)
        # Decider converts risk score into task-specific frame label.
        decision_output = self.decider.decide(fusion_output)
        meta = FrameMeta(
            video_id=frame_ctx.video_id,
            frame_index=frame_ctx.frame_index,
            timestamp_ms=frame_ctx.timestamp_ms,
        )
        return FrameResult(
            meta=meta,
            detector_outputs=detector_outputs,
            fusion=fusion_output,
            decision=decision_output,
        )
