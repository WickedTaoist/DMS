"""
事件级结果结构模块 / Event-level result schema.

本模块定义连续行为事件段的结构，
用于表示一段连续可疑帧形成的行为事件。

This module defines the structure of a continuous behavior event,
which represents a suspicious segment formed by consecutive frames.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class EventResult:
    """
    连续行为事件结果 / Result of one continuous behavior event.

    Attributes:
        event_id: 事件唯一标识。
        video_id: 所属视频 ID。
        event_type: 事件类型。
        start_frame: 起始帧号。
        end_frame: 结束帧号。
        duration_frames: 持续帧数。
        start_ms: 起始毫秒时间。
        end_ms: 结束毫秒时间。
        duration_ms: 持续时间（毫秒）。
        max_risk_score: 事件段内最大风险值。
        mean_risk_score: 事件段内平均风险值。
        evidence_stats: 可选证据统计信息。
        decision_reason: 本事件形成的原因说明。
    """

    # 事件唯一 ID。
    # Unique identifier for the event.
    event_id: str
    # 事件所属视频 ID。
    # Video ID that the event belongs to.
    video_id: str
    # 事件类型，例如 `suspected_phone_use`。
    # Event type such as `suspected_phone_use`.
    event_type: str
    # 起始帧号 / Start frame index.
    start_frame: int
    # 结束帧号 / End frame index.
    end_frame: int
    # 持续帧数 / Event duration in frames.
    duration_frames: int
    # 起始时间戳（毫秒） / Start timestamp in milliseconds.
    start_ms: int
    # 结束时间戳（毫秒） / End timestamp in milliseconds.
    end_ms: int
    # 持续时间（毫秒） / Event duration in milliseconds.
    duration_ms: int
    # 最大风险分数 / Maximum risk score within the event.
    max_risk_score: float
    # 平均风险分数 / Mean risk score within the event.
    mean_risk_score: float
    # 证据统计字典 / Optional evidence statistics.
    evidence_stats: Dict[str, float] = field(default_factory=dict)
    # 形成该事件的原因说明 / Human-readable reason for the event.
    decision_reason: str = ""
