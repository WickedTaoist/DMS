"""
Detector 注册表模块 / Detector registry helpers.

本模块将 detector 名称与具体实现类关联起来，
使系统能够根据配置动态构建 detector 列表。

This module maps detector names to concrete classes so the system
can dynamically build detector instances from configuration.
"""

from typing import Any, Dict, List

from src.detectors.base_detector import BaseDetector
from src.detectors.gaze_detector import GazeDetector
from src.detectors.hand_off_wheel_detector import HandOffWheelDetector
from src.detectors.head_pose_detector import HeadPoseDetector
from src.detectors.phone_detector import PhoneDetector
from src.detectors.vlm_detector import VLMDetector


# 全局 detector 注册表：
# key 是配置里出现的 detector 名字，
# value 是对应的 Python 实现类。
#
# Global detector registry:
# keys are detector names used in config,
# values are the corresponding Python implementation classes.
DETECTOR_REGISTRY = {
    "head_pose": HeadPoseDetector,
    "gaze": GazeDetector,
    "phone": PhoneDetector,
    "hand_off_wheel": HandOffWheelDetector,
    "vlm": VLMDetector,
}


def build_detectors(config: Dict[str, Any]) -> List[BaseDetector]:
    """
    根据配置构建 detector 实例列表 / Build detector instances from config.

    Args:
        config: 全局配置字典。

    Returns:
        已实例化的 detector 对象列表。
        A list of initialized detector objects.
    """
    # 从配置中读取启用的 detector 名称列表。
    # Read the list of enabled detector names from config.
    enabled = config["detectors"]["enabled"]

    # 读取每个 detector 的私有配置块。
    # Read detector-specific config blocks.
    detector_cfg = config["detectors"]["configs"]

    # 收集构建后的 detector 实例。
    # Collect the constructed detector instances.
    detectors: List[BaseDetector] = []

    # 按配置顺序创建 detector，这个顺序也会影响输出顺序。
    # Build detectors in config order, which also affects output ordering.
    for name in enabled:
        # 若配置中出现了未知 detector，则立即报错，避免静默失败。
        # Fail fast when config references an unknown detector.
        if name not in DETECTOR_REGISTRY:
            raise ValueError(f"Unknown detector: {name}")

        # 取出对应的 detector 类。
        # Fetch the corresponding detector class.
        cls = DETECTOR_REGISTRY[name]

        # 使用该 detector 自己的配置块完成实例化。
        # Instantiate the detector with its dedicated config section.
        detectors.append(cls(detector_cfg.get(name, {})))
    return detectors
