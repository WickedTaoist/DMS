import argparse

from src.runners.experiment_runner import run_experiment
from src.runners.run_batch import run_batch
from src.runners.run_single import run_single
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Driver phone usage prototype runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_single = sub.add_parser("single", help="Run one video")
    p_single.add_argument("--input", required=True, help="Input video path")
    p_single.add_argument("--config", required=True, help="YAML config path")

    p_batch = sub.add_parser("batch", help="Run a directory of videos")
    p_batch.add_argument("--input_dir", required=True, help="Input directory path")
    p_batch.add_argument("--config", required=True, help="YAML config path")

    p_exp = sub.add_parser("experiment", help="Run with experiment config")
    p_exp.add_argument("--config", required=True, help="Experiment YAML config path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    logger = setup_logger(config["logging"].get("level", "INFO"), "outputs/logs")

    if args.cmd == "single":
        run_single(args.input, config, logger)
    elif args.cmd == "batch":
        run_batch(args.input_dir, config, logger)
    elif args.cmd == "experiment":
        run_experiment(config, logger)
    else:
        raise ValueError(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    main()
