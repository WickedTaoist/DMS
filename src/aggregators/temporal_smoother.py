"""
时序平滑模块 / Temporal smoothing helpers.

本模块用于降低逐帧标签抖动带来的影响，
例如将两个可疑片段之间非常短的 `normal` 空洞自动填补。

This module reduces frame-level label jitter,
for example by filling very short `normal` gaps between suspicious segments.
"""

from typing import List


def smooth_labels(labels: List[str], max_gap_frames: int) -> List[str]:
    """
    平滑帧级标签序列 / Smooth a frame-level label sequence.

    Args:
        labels: 原始帧标签序列。
        max_gap_frames: 允许填补的最大 normal 间隔长度。

    Returns:
        平滑后的标签序列。
        The smoothed label sequence.
    """
    # 空序列直接返回，避免后续下标访问问题。
    # Return immediately for empty input to avoid index issues later.
    if not labels:
        return labels

    # 复制一份标签，避免原地修改输入序列。
    # Copy the labels so the input sequence is not modified in place.
    smoothed = labels[:]
    n = len(labels)

    # 从第二帧扫描到倒数第二帧，检查中间短缺口。
    # Scan from the second frame to the second-to-last frame to find short gaps.
    for i in range(1, n - 1):
        # 仅在当前位置是 normal，且前一帧已经是可疑时，才有必要检查 gap。
        # Only inspect a gap when the current frame is normal and the previous
        # frame already belongs to a suspicious segment.
        if labels[i] == "normal" and labels[i - 1] != "normal":
            j = i

            # 向后扩展，找到 normal gap 的终点。
            # Expand forward to find the end of the normal gap.
            while j < n and labels[j] == "normal":
                j += 1

            # gap 长度 = 终点 - 起点。
            # Gap length = end index - start index.
            gap = j - i

            # 若 gap 后面还能接上同类可疑段，且 gap 长度不超过阈值，则把 gap 填平。
            # If the gap is followed by another suspicious segment and the gap
            # is short enough, fill it with the preceding suspicious label.
            if j < n and gap <= max_gap_frames and labels[j] != "normal":
                for k in range(i, j):
                    smoothed[k] = labels[i - 1]
    return smoothed
