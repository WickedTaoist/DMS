"""
片段级汇总结构模块 / Clip-level summary schema.

本模块定义整段视频处理完成后的顶层汇总信息，
便于论文实验统计、结果排序与批量分析。

This module defines the top-level summary structure produced after
processing a full video clip, making it suitable for paper analysis,
ranking, and batch-level reporting.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class ClipSummary:
    """
    整视频汇总结果 / Top-level summary for one processed video clip.

    Attributes:
        video_id: 视频标识符。
        total_frames_processed: 实际处理帧数。
        fps_processed: 处理使用的采样 FPS。
        total_duration_ms: 处理视频总时长（毫秒）。
        event_count_suspected_phone_use: 可疑玩手机事件个数。
        event_total_duration_ms: 所有事件总时长。
        event_duration_ratio: 事件总时长占比。
        max_event_duration_ms: 单个事件最大持续时长。
        avg_event_duration_ms: 平均事件时长。
        clip_label: 视频级标签。
        clip_risk_score: 视频级风险分数。
        model_versions: 模型版本信息。
    """

    # 视频 ID / Video identifier.
    video_id: str
    # 实际参与处理的帧数 / Number of frames actually processed.
    total_frames_processed: int
    # 处理阶段使用的采样 FPS / Sampling FPS used during processing.
    fps_processed: float
    # 视频总时长（毫秒） / Total clip duration in milliseconds.
    total_duration_ms: int
    # 可疑玩手机事件数量 / Number of suspected phone-use events.
    event_count_suspected_phone_use: int
    # 全部事件总时长 / Total duration of all events.
    event_total_duration_ms: int
    # 事件总时长占整段视频的比例 / Ratio of event duration to clip duration.
    event_duration_ratio: float
    # 最大单事件时长 / Maximum duration among all events.
    max_event_duration_ms: int
    # 平均事件时长 / Average event duration.
    avg_event_duration_ms: float
    # 视频级标签 / Clip-level label.
    clip_label: str
    # 视频级风险分数 / Clip-level risk score.
    clip_risk_score: float
    # 记录模型版本，便于复现实验 / Model versions for reproducibility.
    model_versions: Dict[str, str] = field(default_factory=dict)
