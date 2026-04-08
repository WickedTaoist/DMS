"""
公共数据结构模块 / Common schema definitions.

本模块定义多个子模块都会用到的基础数据结构，
例如帧元信息、目标框以及统一 detector 输出格式。

This module defines shared data structures used across the project,
such as frame metadata, bounding boxes, and the unified detector output.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(slots=True)
class FrameMeta:
    """
    单帧基础元信息 / Basic metadata for one decoded frame.

    Attributes:
        video_id: 视频标识符。
        frame_index: 帧序号。
        timestamp_ms: 帧时间戳（毫秒）。
    """

    # 当前帧所属的视频 ID。
    # The video ID that this frame belongs to.
    video_id: str

    # 当前帧在原始视频中的索引。
    # The frame index in the original video.
    frame_index: int

    # 当前帧对应的毫秒时间戳。
    # The frame timestamp in milliseconds.
    timestamp_ms: int


@dataclass(slots=True)
class BBox:
    """
    矩形框结构 / Bounding box in `xyxy` format.

    `xyxy` 表示左上角 `(x1, y1)` 和右下角 `(x2, y2)`。
    `xyxy` means top-left `(x1, y1)` and bottom-right `(x2, y2)`.
    """

    # 左上角 x 坐标 / Top-left x coordinate.
    x1: float
    # 左上角 y 坐标 / Top-left y coordinate.
    y1: float
    # 右下角 x 坐标 / Bottom-right x coordinate.
    x2: float
    # 右下角 y 坐标 / Bottom-right y coordinate.
    y2: float
    # 检测分数 / Detection confidence score.
    score: float
    # 类别名 / Class label name.
    label: str


@dataclass(slots=True)
class DetectorOutput:
    """
    统一 detector 输出封装 / Unified detector output envelope.

    设计此结构的目的是让所有 detector 都遵循同一个输出接口，
    这样 pipeline、fusion、decision 层就不需要依赖具体模型实现。

    The purpose of this structure is to make all detectors follow the same
    output contract, so pipeline, fusion, and decision layers do not depend
    on model-specific implementations.
    """

    # 输出来自哪个 detector。
    # Name of the detector that produced this output.
    detector_name: str

    # 本次推理是否成功。
    # Whether the inference succeeded.
    success: bool

    # 推理耗时（毫秒）。
    # Inference latency in milliseconds.
    latency_ms: float

    # 整体置信度，可为空。
    # Optional overall confidence score.
    confidence: Optional[float]

    # 具体 detector 的原始载荷数据。
    # Raw detector-specific payload.
    payload: Dict[str, Any]

    # 若失败，可记录错误信息。
    # Optional error message if inference failed.
    error: Optional[str] = None
