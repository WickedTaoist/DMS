"""
阈值策略结构模块 / Threshold policy schema.

本模块用于集中描述判定与时序聚合相关的关键阈值。
虽然当前项目主要从 YAML 读取配置，但保留该结构体有利于后续
进行更强约束的配置校验和实验参数传递。

This module centralizes key thresholds related to decision and
temporal aggregation. Although the current project mostly reads
config directly from YAML, this dataclass is useful for stronger
validation and cleaner parameter passing in future iterations.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ThresholdPolicy:
    """
    判定与聚合阈值集合 / Collection of decision and aggregation thresholds.

    Attributes:
        frame_risk_threshold: 帧级风险阈值。
        min_event_frames: 形成有效事件的最短帧数。
        max_gap_frames: 时序平滑时可填补的最大 normal 间隔。
    """

    # 风险分数达到该阈值时，帧会被标为可疑。
    # A frame is marked suspicious when its risk score reaches this threshold.
    frame_risk_threshold: float = 0.6

    # 连续可疑帧少于该阈值时，不构成有效事件。
    # Suspicious segments shorter than this threshold are discarded.
    min_event_frames: int = 8

    # 时间平滑允许填补的最大空洞长度。
    # Maximum gap length that temporal smoothing is allowed to bridge.
    max_gap_frames: int = 3
