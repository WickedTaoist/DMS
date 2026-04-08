"""
视频文件名解析模块 / Video filename parsing helpers.

本模块用于把实验视频文件名解析成结构化元信息，
例如视频 ID、原始文件名以及粗粒度标签。

This module converts experiment video filenames into structured
metadata such as video ID, original filename, and coarse labels.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class VideoNameInfo:
    """
    文件名解析结果 / Parsed metadata extracted from a video filename.

    Attributes:
        video_id: 适合输出文件和汇总表使用的稳定视频标识。
        file_name: 原始文件名。
        parsed_label: 根据命名规则推断出的粗粒度标签。
    """

    # `video_id` 通常使用去后缀的文件名。
    # `video_id` is typically the filename stem without extension.
    video_id: str

    # 原始文件名，保留给汇总表和追溯分析使用。
    # Keep the original filename for batch summary and traceability.
    file_name: str

    # 解析得到的类别标签，例如 `clear_phone_use`。
    # Parsed coarse label such as `clear_phone_use`.
    parsed_label: str


class VideoNameParser:
    """
    文件名标签解析器 / Filename-based coarse label parser.

    设计目标：
    1. 不把数据集命名规则写死在 runner 中
    2. 便于未来增加更多命名模式
    3. 让批量汇总逻辑保持干净

    Design goals:
    1. Keep dataset naming rules out of runner modules
    2. Make it easy to extend naming rules later
    3. Keep batch summary logic clean and focused
    """

    def __init__(self) -> None:
        # 规则顺序很重要：更具体的类别要放在前面。
        # Rule order matters: more specific patterns should come first.
        self._rules: list[tuple[str, str]] = [
            ("后排乘客玩手机", "rear_passenger_phone_use"),
            ("明确玩手机", "clear_phone_use"),
            ("疑似玩手机", "suspected_phone_use"),
            ("正常驾驶", "normal_driving"),
        ]

    def parse(self, file_path: str) -> VideoNameInfo:
        """
        解析单个视频路径 / Parse one video path into structured metadata.

        Args:
            file_path: 输入视频路径。

        Returns:
            `VideoNameInfo` 对象，包含视频 ID、原始文件名和解析标签。
            A `VideoNameInfo` object containing video ID, filename, and parsed label.
        """
        # 提取原始文件名，例如 `std_明确玩手机1.mp4`。
        # Extract the original filename, e.g. `std_明确玩手机1.mp4`.
        file_name = Path(file_path).name

        # 提取不带扩展名的主干，便于当作 video_id 使用。
        # Extract the extension-free stem for use as `video_id`.
        stem = Path(file_path).stem

        # 按命名规则推断标签。
        # Infer the label according to filename rules.
        parsed_label = self._infer_label(file_name)

        # 返回统一结构化对象，供 batch runner 直接消费。
        # Return a structured object that can be consumed by the batch runner.
        return VideoNameInfo(video_id=stem, file_name=file_name, parsed_label=parsed_label)

    def _infer_label(self, file_name: str) -> str:
        """
        根据文件名推断标签 / Infer a label from the filename.

        若没有匹配到任何规则，则返回 `unknown`。
        Returns `unknown` when no rule matches.
        """
        # 按顺序尝试规则匹配。
        # Match rules in order.
        for key, label in self._rules:
            if key in file_name:
                return label

        # 未命中任何规则时返回未知标签。
        # Return a fallback unknown label when no rule is matched.
        return "unknown"
