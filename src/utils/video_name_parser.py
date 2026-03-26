from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class VideoNameInfo:
    """Normalized metadata parsed from an input video filename."""

    video_id: str
    file_name: str
    parsed_label: str


class VideoNameParser:
    """
    Parse filename text into a coarse experiment label for batch analysis.

    Rules are intentionally centralized in this utility to avoid embedding
    dataset-specific assumptions directly inside runner modules.
    """

    def __init__(self) -> None:
        # Rule order matters: more specific conditions first.
        self._rules: list[tuple[str, str]] = [
            ("后排乘客玩手机", "rear_passenger_phone_use"),
            ("明确玩手机", "clear_phone_use"),
            ("疑似玩手机", "suspected_phone_use"),
            ("正常驾驶", "normal_driving"),
        ]

    def parse(self, file_path: str) -> VideoNameInfo:
        """Parse `video_id`, original filename, and coarse label."""
        file_name = Path(file_path).name
        stem = Path(file_path).stem
        parsed_label = self._infer_label(file_name)
        return VideoNameInfo(video_id=stem, file_name=file_name, parsed_label=parsed_label)

    def _infer_label(self, file_name: str) -> str:
        for key, label in self._rules:
            if key in file_name:
                return label
        return "unknown"
