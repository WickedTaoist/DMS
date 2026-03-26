import logging
from pathlib import Path


def setup_logger(level: str, output_dir: str) -> logging.Logger:
    """Initialize a simple console+file logger for experiment runs."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("driver_phone_usage")
    logger.setLevel(level.upper())
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    file_handler = logging.FileHandler(Path(output_dir) / "run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def attach_file_logger(logger: logging.Logger, file_path: str) -> None:
    """
    Attach an extra file handler if the same target is not already attached.

    Useful for mode-specific logs such as `run_batch.log`.
    """
    target = str(Path(file_path).resolve())
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler) and str(Path(handler.baseFilename).resolve()) == target:
            return
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
