"""
OpenVINO 头姿 detector / OpenVINO-based head-pose detector.
"""

from pathlib import Path
from time import perf_counter
from typing import Any

import cv2
import numpy as np

from src.detectors.base_detector import BaseDetector, FrameContext
from src.schemas.common import DetectorOutput
from src.utils.path_utils import resolve_project_path


class HeadPoseDetector(BaseDetector):
    """基于 OpenVINO `head-pose-estimation-adas-0001` 的头姿检测器。"""

    name = "head_pose"

    def setup(self) -> None:
        """加载 OpenVINO 模型与人脸检测器。"""
        try:
            from openvino import Core
        except ImportError as exc:
            raise ImportError(
                "OpenVINO is required for head_pose detector. Install with `pip install openvino`."
            ) from exc

        model_path = resolve_project_path(self.config.get("model_path", "models/openvino/head_pose.xml"))
        if not model_path.exists():
            raise FileNotFoundError(f"Head-pose model not found: {model_path}")

        self._device = str(self.config.get("device", "CPU")).upper()
        self._pitch_down_threshold = float(self.config.get("pitch_down_threshold", 15.0))
        self._face_padding_ratio = float(self.config.get("face_padding_ratio", 0.2))

        core = Core()
        ov_model = core.read_model(model=model_path)
        self._compiled_model = core.compile_model(model=ov_model, device_name=self._device)
        self._infer_request = self._compiled_model.create_infer_request()
        self._input = self._compiled_model.input(0)
        self._input_h, self._input_w = int(self._input.shape[2]), int(self._input.shape[3])
        self._output_names = {out.get_any_name(): out for out in self._compiled_model.outputs}

        # 优先使用 Haar 人脸检测，失败时退化为中心裁剪。
        haar_path = str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
        self._face_cascade = cv2.CascadeClassifier(haar_path)
        if self._face_cascade.empty():
            self._face_cascade = None

    def _extract_face_roi(self, frame_bgr: np.ndarray) -> tuple[np.ndarray, float]:
        """提取人脸区域并返回置信度估计。"""
        h, w = frame_bgr.shape[:2]
        if self._face_cascade is not None:
            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            faces = self._face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
            if len(faces) > 0:
                x, y, fw, fh = max(faces, key=lambda box: box[2] * box[3])
                pad_w = int(fw * self._face_padding_ratio)
                pad_h = int(fh * self._face_padding_ratio)
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(w, x + fw + pad_w)
                y2 = min(h, y + fh + pad_h)
                return frame_bgr[y1:y2, x1:x2], 0.9

        # 没有人脸时采用中心区域，保证管线可持续运行。
        crop_w = int(w * 0.45)
        crop_h = int(h * 0.45)
        x1 = (w - crop_w) // 2
        y1 = (h - crop_h) // 2
        x2 = x1 + crop_w
        y2 = y1 + crop_h
        return frame_bgr[y1:y2, x1:x2], 0.3

    def _preprocess(self, face_bgr: np.ndarray) -> np.ndarray:
        face_resized = cv2.resize(face_bgr, (self._input_w, self._input_h), interpolation=cv2.INTER_LINEAR)
        chw = np.transpose(face_resized, (2, 0, 1))
        return np.expand_dims(chw, axis=0).astype(np.float32)

    def _read_angle(self, output_name: str, outputs: dict[Any, np.ndarray]) -> float:
        port = self._output_names[output_name]
        val = outputs[port].reshape(-1)[0]
        return float(val)

    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        t0 = perf_counter()
        try:
            frame = frame_ctx.frame_bgr
            if frame is None:
                raise ValueError("Empty frame received")

            face_roi, face_conf = self._extract_face_roi(frame)
            input_blob = self._preprocess(face_roi)
            raw_outputs = self._infer_request.infer({self._input: input_blob})

            pitch = self._read_angle("angle_p_fc", raw_outputs)
            yaw = self._read_angle("angle_y_fc", raw_outputs)
            roll = self._read_angle("angle_r_fc", raw_outputs)
            is_head_down = pitch >= self._pitch_down_threshold

            latency_ms = (perf_counter() - t0) * 1000.0
            return DetectorOutput(
                detector_name=self.name,
                success=True,
                latency_ms=latency_ms,
                confidence=face_conf,
                payload={
                    "pitch": pitch,
                    "yaw": yaw,
                    "roll": roll,
                    "is_head_down": is_head_down,
                    "model": "head-pose-estimation-adas-0001",
                },
            )
        except Exception as exc:
            latency_ms = (perf_counter() - t0) * 1000.0
            return DetectorOutput(
                detector_name=self.name,
                success=False,
                latency_ms=latency_ms,
                confidence=None,
                payload={"pitch": 0.0, "yaw": 0.0, "roll": 0.0, "is_head_down": False},
                error=str(exc),
            )

    def teardown(self) -> None:
        self._compiled_model = None
        self._infer_request = None
