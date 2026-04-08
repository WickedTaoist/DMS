"""
标识符工具模块 / Identifier utility helpers.

本文件负责生成项目中的稳定 ID，例如事件段 ID。
这些 ID 不追求密码学安全性，而追求：
1. 可复现
2. 简洁
3. 对实验结果友好

This module generates stable identifiers used in the project,
such as event IDs. The IDs are not designed for cryptographic
security, but for reproducibility, compactness, and experiment tracking.
"""

import hashlib


def make_event_id(video_id: str, start_idx: int, end_idx: int) -> str:
    """
    为事件段生成稳定 ID / Generate a stable ID for one event segment.

    Args:
        video_id: 视频标识符。
        start_idx: 事件起始帧在结果序列中的位置。
        end_idx: 事件结束帧在结果序列中的位置。

    Returns:
        形如 `evt_xxxxx` 的短 ID。
        A compact ID in the format `evt_xxxxx`.
    """
    # 将关键定位信息拼接为一个唯一字符串种子。
    # Concatenate location-defining fields into a unique seed string.
    seed = f"{video_id}:{start_idx}:{end_idx}".encode("utf-8")

    # 使用 MD5 取前 10 位十六进制摘要，足够实验场景使用。
    # Use the first 10 hex digits of MD5, which is sufficient for experiments.
    digest = hashlib.md5(seed).hexdigest()[:10]

    # 给事件 ID 加上统一前缀，便于识别。
    # Add a consistent prefix so event IDs are easy to recognize.
    return f"evt_{digest}"
