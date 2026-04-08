"""
路径工具模块 / Path utility helpers.

本模块负责：
1. 统一定位项目根目录
2. 将配置中的相对路径解析为绝对路径
3. 对输入目录做前置校验

This module is responsible for:
1. Locating the project root directory
2. Resolving relative config paths into absolute paths
3. Validating required input directories before execution
"""

from pathlib import Path


def get_project_root() -> Path:
    """
    获取项目根目录 / Get the project root directory.

    当前文件位于 `src/utils/path_utils.py`，
    因此向上两层即可到达项目根目录。

    This file lives at `src/utils/path_utils.py`,
    so going up two parent levels reaches the project root.
    """
    # `resolve()` 可以消除符号链接与相对路径影响。
    # `resolve()` normalizes symlinks and relative path segments.
    return Path(__file__).resolve().parents[2]


def resolve_project_path(path_str: str) -> Path:
    """
    解析项目路径 / Resolve a project-relative path.

    Args:
        path_str: 来自配置或命令行的路径字符串。

    Returns:
        若输入为绝对路径，则原样返回；
        若输入为相对路径，则按项目根目录解析。

        If the input is already absolute, return it as-is;
        otherwise resolve it relative to the project root.
    """
    # 先构造 Path 对象，统一后续处理。
    # Convert the input string into a Path object first.
    path = Path(path_str)

    # 绝对路径直接使用，避免重复拼接项目根目录。
    # Absolute paths should be used directly.
    if path.is_absolute():
        return path

    # 相对路径统一以项目根目录为基准，保证 runner 行为稳定。
    # Resolve relative paths against project root for stable runner behavior.
    return (get_project_root() / path).resolve()


def ensure_directory_exists(path: Path, description: str) -> None:
    """
    检查目录是否存在 / Ensure a required directory exists.

    Args:
        path: 需要检查的目录路径。
        description: 用于报错提示的人类可读描述。
    """
    # 如果目标不存在或不是目录，则立即抛出清晰错误。
    # Raise a clear error immediately if the target is missing or not a directory.
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"{description} does not exist or is not a directory: {path}")
