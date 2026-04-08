"""
日志工具模块 / Logging utility helpers.

本模块负责初始化统一日志器，并根据运行模式追加不同日志文件。
科研原型阶段使用标准库 `logging` 即可满足需求，便于轻量维护。

This module initializes the shared project logger and attaches
extra log files for different execution modes. The standard
library `logging` module is sufficient for this research prototype.
"""

import logging
from pathlib import Path


def setup_logger(level: str, output_dir: str) -> logging.Logger:
    """
    初始化项目主日志器 / Initialize the main project logger.

    Args:
        level: 日志等级，例如 `INFO`、`DEBUG`。
        output_dir: 日志输出目录。

    Returns:
        配置完成的 `logging.Logger` 实例。
        A configured `logging.Logger` instance.
    """
    # 确保日志目录存在，避免 FileHandler 创建失败。
    # Ensure the log directory exists before creating file handlers.
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 使用固定名称，保证整个项目复用同一个逻辑日志器。
    # Use a fixed logger name so all modules share the same logical logger.
    logger = logging.getLogger("driver_phone_usage")

    # 设置全局日志等级。
    # Set the overall logging level.
    logger.setLevel(level.upper())

    # 清空旧 handler，避免重复初始化时日志输出多次。
    # Clear existing handlers to avoid duplicate log lines.
    logger.handlers.clear()

    # 统一日志格式：时间 | 等级 | 消息。
    # Shared log format: timestamp | level | message.
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # 控制台日志，便于实时查看执行进度。
    # Console logging for real-time progress monitoring.
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 默认文件日志，用于保留完整运行记录。
    # Default file log used to preserve a full execution trace.
    file_handler = logging.FileHandler(Path(output_dir) / "run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def attach_file_logger(logger: logging.Logger, file_path: str) -> None:
    """
    附加额外文件日志 / Attach an extra file log handler.

    主要用于像 `run_batch.log` 这样的模式专属日志文件。
    如果同一路径的文件日志已经存在，则不会重复附加。

    This is mainly used for mode-specific log files such as `run_batch.log`.
    If the same file handler already exists, it will not be attached again.
    """
    # 解析目标文件的绝对路径，用于和已存在 handler 做精确比对。
    # Resolve the target file to an absolute path for exact handler matching.
    target = str(Path(file_path).resolve())

    # 遍历现有 handler，若同目标文件已存在，则直接返回。
    # Scan existing handlers and return early if the same file is already attached.
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler) and str(Path(handler.baseFilename).resolve()) == target:
            return

    # 确保目标日志目录存在。
    # Ensure the parent directory for the target log file exists.
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    # 额外文件日志沿用统一格式。
    # Reuse the same formatter for the extra file logger.
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
