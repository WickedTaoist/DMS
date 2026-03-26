from pathlib import Path


def get_project_root() -> Path:
    """
    Return the repository root based on the current source tree location.

    The file lives at `src/utils/path_utils.py`, therefore `parents[2]`
    points to the project root directory.
    """
    return Path(__file__).resolve().parents[2]


def resolve_project_path(path_str: str) -> Path:
    """
    Resolve a path string to an absolute path under project root.

    Absolute input paths are returned as-is. Relative paths are resolved
    against the project root to keep config behavior stable across runners.
    """
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (get_project_root() / path).resolve()


def ensure_directory_exists(path: Path, description: str) -> None:
    """Raise a clear error when required input directory is missing."""
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"{description} does not exist or is not a directory: {path}")
