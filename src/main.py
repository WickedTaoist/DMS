"""
项目命令行入口模块 / Command-line entrypoint for the project.

本模块负责：
1. 解析命令行参数
2. 加载配置
3. 初始化日志
4. 把执行流分发到 single / batch / experiment runner

This module is responsible for:
1. Parsing command-line arguments
2. Loading configuration
3. Initializing logging
4. Dispatching execution to single / batch / experiment runners
"""

import argparse

from src.runners.experiment_runner import run_experiment
from src.runners.run_batch import run_batch
from src.runners.run_single import run_single
from src.utils.config_loader import load_config
from src.utils.logger import attach_file_logger, setup_logger
from src.utils.path_utils import resolve_project_path


def build_parser() -> argparse.ArgumentParser:
    """
    构建命令行解析器 / Build the command-line argument parser.

    Returns:
        配置完成的 `ArgumentParser`。
        A fully configured `ArgumentParser`.
    """
    # 创建顶层解析器，描述整个科研原型项目。
    # Create the top-level parser describing the research prototype.
    parser = argparse.ArgumentParser(description="Driver phone usage prototype runner")

    # 使用子命令区分 single / batch / experiment 三种运行模式。
    # Use subcommands to separate single / batch / experiment modes.
    sub = parser.add_subparsers(dest="cmd", required=True)

    # `single`：处理单个视频。
    # `single`: process one input video.
    p_single = sub.add_parser("single", help="Run one video")
    p_single.add_argument("--input", required=True, help="Input video path")
    p_single.add_argument("--config", required=True, help="YAML config path")

    # `batch`：批量处理目录中的视频。
    # `batch`: process all videos in a directory.
    p_batch = sub.add_parser("batch", help="Run a directory of videos")
    p_batch.add_argument("--input_dir", required=False, default=None, help="Optional input directory override")
    p_batch.add_argument("--config", required=True, help="YAML config path")

    # `experiment`：根据实验配置进行运行。
    # `experiment`: run based on experiment configuration.
    p_exp = sub.add_parser("experiment", help="Run with experiment config")
    p_exp.add_argument("--config", required=True, help="Experiment YAML config path")
    return parser


def main() -> None:
    """
    主函数 / Main function.

    该函数是项目命令执行的实际起点。
    This function is the real starting point of command execution.
    """
    # 构建解析器并读取命令行参数。
    # Build the parser and parse command-line arguments.
    parser = build_parser()
    args = parser.parse_args()

    # 从 YAML 读取配置，并处理继承与路径解析。
    # Load YAML config and handle inheritance plus path resolution.
    config = load_config(args.config)

    # 根据配置解析输出根目录，再定位日志目录。
    # Resolve the output root from config, then derive the logs directory.
    output_root = resolve_project_path(config.get("output", {}).get("root_dir", "outputs"))
    logs_dir = output_root / "logs"

    # 初始化项目统一日志器。
    # Initialize the shared project logger.
    logger = setup_logger(config["logging"].get("level", "INFO"), str(logs_dir))

    # 根据子命令分发到不同 runner。
    # Dispatch to different runners based on the selected subcommand.
    if args.cmd == "single":
        run_single(args.input, config, logger)
    elif args.cmd == "batch":
        # batch 模式额外记录独立日志文件，方便实验追踪。
        # Attach an additional batch-specific log file for experiment tracking.
        attach_file_logger(logger, str(logs_dir / "run_batch.log"))
        run_batch(config, logger, input_dir_override=args.input_dir)
    elif args.cmd == "experiment":
        run_experiment(config, logger)
    else:
        # 理论上 argparse 已限制住命令分支，这里属于防御性检查。
        # In theory argparse already constrains the valid branches;
        # this is a defensive safeguard.
        raise ValueError(f"Unknown command: {args.cmd}")


# 允许使用 `python -m src.main` 的方式执行。
# Allow execution via `python -m src.main`.
if __name__ == "__main__":
    main()
