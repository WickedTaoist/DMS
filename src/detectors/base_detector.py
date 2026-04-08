"""
Detector 抽象接口模块 / Base abstractions for detector plugins.

本模块定义：
1. `FrameContext`：传递给 detector 的统一帧上下文
2. `BaseDetector`：所有 detector 必须遵守的生命周期接口

This module defines:
1. `FrameContext`: the unified per-frame context passed to detectors
2. `BaseDetector`: the lifecycle interface all detectors must follow
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

from src.schemas.common import DetectorOutput


@dataclass(slots=True)
class FrameContext:
    """
    传递给 detector 的统一帧上下文 / Unified frame context passed to detectors.

    Attributes:
        video_id: 视频标识符。
        frame_index: 帧索引。
        timestamp_ms: 帧时间戳（毫秒）。
        frame_bgr: OpenCV BGR 图像数据。
    """

    # 当前帧所属视频 ID。
    # Video ID that this frame belongs to.
    video_id: str

    # 当前帧在视频中的索引。
    # Frame index inside the video.
    frame_index: int

    # 当前帧时间戳（毫秒）。
    # Frame timestamp in milliseconds.
    timestamp_ms: int

    # 原始 BGR 图像，供 OpenCV / OpenVINO / YOLO 等后续模型使用。
    # Raw BGR image for later use by OpenCV / OpenVINO / YOLO and others.
    frame_bgr: Any


class BaseDetector(ABC):
    """
    Detector 插件抽象基类 / Abstract base class for detector plugins.

    设计目标：
    1. 屏蔽不同模型框架的差异
    2. 保持 pipeline 对 detector 的调用方式一致
    3. 让后续新增 detector 时不需要重构主流程

    Design goals:
    1. Hide differences between model frameworks
    2. Keep detector invocation consistent in the pipeline
    3. Avoid refactoring the main flow when adding new detectors
    """

    # 每个 detector 需要提供一个稳定名称。
    # Each detector should expose a stable name.
    name: str

    def __init__(self, config: Dict[str, Any]) -> None:
        # 保存 detector 私有配置。
        # Store detector-specific config.
        self.config = config

    @abstractmethod
    def setup(self) -> None:
        """
        初始化资源 / Initialize runtime resources.

        通常在这里加载模型、权重、推理引擎或其他依赖。
        This is typically where models, weights, engines, or dependencies are loaded.
        """

    @abstractmethod
    def infer(self, frame_ctx: FrameContext) -> DetectorOutput:
        """
        执行单帧推理 / Run per-frame inference.

        Args:
            frame_ctx: 标准化后的帧上下文。

        Returns:
            统一结构化的 `DetectorOutput`。
            A normalized `DetectorOutput`.
        """

    @abstractmethod
    def teardown(self) -> None:
        """
        释放资源 / Release runtime resources.

        通常用于关闭推理引擎、释放句柄或显存。
        Typically used to free engines, handles, or GPU memory.
        """
