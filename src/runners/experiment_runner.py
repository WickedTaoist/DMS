from typing import Any, Dict

from src.runners.run_batch import run_batch
from src.runners.run_single import run_single


def run_experiment(config: Dict[str, Any], logger) -> None:
    """Run one experiment config in single or batch mode."""
    mode = config.get("input", {}).get("mode", "batch")
    if mode == "single":
        video_path = config.get("input", {}).get("video_path", "")
        run_single(video_path, config, logger)
        return
    if mode == "batch":
        run_batch(config, logger)
        return
    raise ValueError(f"Unsupported input mode: {mode}")
