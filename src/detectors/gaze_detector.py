"""L2CS-Net 视线 detector / L2CS-Net-based gaze detector."""

from time import perf_counter
from typing import Any

import cv2  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput
from src.utils.path_utils import resolve_project_path


class GazeDetector(BaseDetector):
    """基于 L2CS-Net 的视线检测器。"""

    name = "gaze"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self._gaze_down_threshold = 10.0
        self._downward_positive = True
        self._confidence_threshold = 0.5
        self._arch = "ResNet50"
        self._pipeline: Any = None
        self._torch_device: Any = None

    def setup(self) -> None:
        """加载 L2CS-Net 权重与 RetinaFace 人脸检测器。"""
        try:
            import torch
            from l2cs import Pipeline
        except ImportError as exc:
            raise ImportError(
                "L2CS-Net is required for gaze detector. Install with "
                "`pip install git+https://github.com/Ahmednull/L2CS-Net.git`."
            ) from exc

        model_path = resolve_project_path(
            self.config.get("model_path", "models/l2cs/Gaze360/L2CSNet_gaze360.pkl")
        )
        if not model_path.exists():
            raise FileNotFoundError(
                f"L2CS gaze model not found: {model_path}. "
                "Run `python scripts/download_l2cs_gaze.py` first."
            )

        self._gaze_down_threshold = float(self.config.get("gaze_down_threshold", 10.0))
        self._downward_positive = bool(self.config.get("downward_positive", True))
        self._confidence_threshold = float(self.config.get("confidence_threshold", 0.5))
        self._arch = str(self.config.get("arch", "ResNet50"))
        self._torch_device = self._resolve_torch_device(torch, self.config.get("device", "cpu"))

        self._pipeline = Pipeline(
            weights=model_path,
            arch=self._arch,
            device=self._torch_device,
            include_detector=True,
            confidence_threshold=self._confidence_threshold,
        )

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """执行单帧视线推理 / Run gaze inference on a single frame."""
        t0 = perf_counter()
        try:
            frame = frame_ctx.frame_bgr
            if frame is None:
                raise ValueError("Empty frame received")

            gaze_pitch, gaze_yaw, gaze_vector, face_conf = self._estimate_gaze(frame)
            is_gaze_down = self._is_gaze_down(gaze_pitch)
            latency_ms = (perf_counter() - t0) * 1000.0

            return DetectorOutput(
                detector_name=self.name,
                success=True,
                latency_ms=latency_ms,
                confidence=face_conf,
                payload={
                    "gaze_pitch": gaze_pitch,
                    "gaze_yaw": gaze_yaw,
                    "gaze_vector": gaze_vector,
                    "is_gaze_down": is_gaze_down,
                    "downward_positive": self._downward_positive,
                    "model": "L2CSNet_gaze360",
                },
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            latency_ms = (perf_counter() - t0) * 1000.0
            return DetectorOutput(
                detector_name=self.name,
                success=False,
                latency_ms=latency_ms,
                confidence=None,
                payload={
                    "gaze_pitch": 0.0,
                    "gaze_yaw": 0.0,
                    "gaze_vector": [0.0, 0.0, 0.0],
                    "is_gaze_down": False,
                    "downward_positive": self._downward_positive,
                    "model": "L2CSNet_gaze360",
                },
                error=str(exc),
            )

    def _estimate_gaze(self, frame_bgr: np.ndarray) -> tuple[float, float, list[float], float]:
        """Run L2CS-Net and return pitch/yaw in degrees plus 3D gaze vector."""
        from l2cs.utils import gazeto3d

        results = self._safe_step(frame_bgr)
        if results is None:
            raise ValueError("No face detected for gaze estimation")

        face_idx = self._select_primary_face(results.bboxes)
        pitch_rad = float(np.asarray(results.pitch).reshape(-1)[face_idx])
        yaw_rad = float(np.asarray(results.yaw).reshape(-1)[face_idx])
        gaze_pitch = float(np.degrees(pitch_rad))
        gaze_yaw = float(np.degrees(yaw_rad))
        gaze_vector = gazeto3d(np.array([yaw_rad, pitch_rad], dtype=np.float64)).astype(float).tolist()

        scores = np.asarray(results.scores).reshape(-1)
        face_conf = float(scores[face_idx]) if scores.size else 0.5
        return gaze_pitch, gaze_yaw, gaze_vector, face_conf

    def _safe_step(self, frame_bgr: np.ndarray) -> Any:
        """Call L2CS pipeline.step while handling the no-face empty-stack bug."""
        try:
            results = self._pipeline.step(frame_bgr)
        except ValueError:
            return None
        if np.asarray(results.pitch).size == 0:
            return None
        return results

    @staticmethod
    def _select_primary_face(bboxes: np.ndarray) -> int:
        """Pick the largest detected face, which is usually the driver."""
        boxes = np.asarray(bboxes).reshape(-1, 4)
        if boxes.shape[0] == 1:
            return 0
        areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        return int(np.argmax(areas))

    def _is_gaze_down(self, gaze_pitch: float) -> bool:
        """Convert gaze pitch to down-look boolean with configurable sign."""
        if self._downward_positive:
            return gaze_pitch >= self._gaze_down_threshold
        return gaze_pitch <= -self._gaze_down_threshold

    @staticmethod
    def _resolve_torch_device(torch_mod: Any, device_cfg: Any) -> Any:
        """Map project device strings to torch.device."""
        raw = str(device_cfg).strip().lower()
        if raw in {"", "cpu"}:
            return torch_mod.device("cpu")
        if raw in {"gpu", "cuda"}:
            return torch_mod.device("cuda:0")
        if raw.isdigit():
            return torch_mod.device(f"cuda:{raw}")
        if raw.startswith("cuda"):
            return torch_mod.device(raw)
        return torch_mod.device("cpu")

    def teardown(self) -> None:
        """释放视线 detector 资源 / Release gaze detector resources."""
        self._pipeline = None
        self._torch_device = None
