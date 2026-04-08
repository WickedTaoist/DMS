"""
事件聚合模块 / Event aggregation helpers.

本模块把帧级标签序列聚合为连续事件段，
便于后续做 clip-level 汇总和论文事件级统计。

This module aggregates frame-level labels into continuous event segments,
which is useful for clip-level summaries and event-level paper analysis.
"""

from typing import List

from src.schemas.event_result import EventResult
from src.schemas.frame_result import FrameResult
from src.utils.id_utils import make_event_id


def aggregate_events(
    frame_results: List[FrameResult], min_event_frames: int, target_label: str = "suspected_phone_use"
) -> List[EventResult]:
    """
    将帧级标签序列聚合为事件列表 / Aggregate frame labels into event segments.

    Args:
        frame_results: 按时间排序的帧级结果列表。
        min_event_frames: 形成有效事件所需的最短持续帧数。
        target_label: 被视为目标事件的帧标签。
    """
    # 收集最终生成的事件。
    # Collect the final event results.
    events: List[EventResult] = []

    # `start_idx` 记录当前正在构建的事件起点。
    # `start_idx` tracks the start position of the current active event.
    start_idx = None

    # 顺序扫描帧级结果，识别连续 target_label 片段。
    # Scan frame results sequentially to find continuous target-label segments.
    for i, fr in enumerate(frame_results):
        label = fr.decision.get("frame_label", "normal")

        # 当遇到 target_label 且当前未处于事件中时，记录起点。
        # When entering a target segment, store its starting index.
        if label == target_label and start_idx is None:
            start_idx = i

        # 当离开 target_label 且之前已有起点时，说明一个事件结束了。
        # When leaving a target segment after having a start index,
        # a full event segment has ended.
        if label != target_label and start_idx is not None:
            _flush_event(frame_results, start_idx, i - 1, min_event_frames, events)
            start_idx = None

    # 若扫描结束时仍处于事件中，则补写最后一个事件。
    # If the scan ends while an event is still active, flush the last event.
    if start_idx is not None:
        _flush_event(frame_results, start_idx, len(frame_results) - 1, min_event_frames, events)
    return events


def _flush_event(
    frame_results: List[FrameResult],
    start_idx: int,
    end_idx: int,
    min_event_frames: int,
    out_events: List[EventResult],
) -> None:
    """
    将一个候选区间写入事件列表 / Convert a candidate segment into an event result.

    该函数只在候选段长度达到 `min_event_frames` 时才会真正生成事件。
    This helper only emits an event when the candidate segment is long enough.
    """
    # 计算当前候选事件的长度（帧数）。
    # Compute the current candidate event length in frames.
    length = end_idx - start_idx + 1

    # 若长度不足阈值，则视为噪声，不输出事件。
    # Discard the candidate as noise if it is shorter than the threshold.
    if length < min_event_frames:
        return

    # 切出该事件段对应的帧结果。
    # Slice the frame results belonging to this event segment.
    chunk = frame_results[start_idx : end_idx + 1]

    # 提取事件段内每一帧的风险分数，供统计使用。
    # Extract per-frame risk scores within the event for later statistics.
    scores = [float(x.fusion.get("risk_score", 0.0)) for x in chunk]

    # 读取视频 ID 与时间边界。
    # Read video ID and temporal boundaries.
    video_id = chunk[0].meta.video_id
    start_ms = chunk[0].meta.timestamp_ms
    end_ms = chunk[-1].meta.timestamp_ms

    # 构造结构化事件对象并加入输出列表。
    # Build the structured event object and append it to the output list.
    out_events.append(
        EventResult(
            event_id=make_event_id(video_id, start_idx, end_idx),
            video_id=video_id,
            event_type="suspected_phone_use",
            start_frame=chunk[0].meta.frame_index,
            end_frame=chunk[-1].meta.frame_index,
            duration_frames=length,
            start_ms=start_ms,
            end_ms=end_ms,
            duration_ms=max(0, end_ms - start_ms),
            max_risk_score=max(scores) if scores else 0.0,
            mean_risk_score=(sum(scores) / len(scores)) if scores else 0.0,
            evidence_stats={},
            decision_reason="rule_based_temporal_aggregation",
        )
    )
