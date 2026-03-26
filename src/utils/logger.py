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
