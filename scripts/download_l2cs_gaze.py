"""
Download L2CS-Net Gaze360 pretrained weights.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# Official L2CS-Net Gaze360 weight (Google Drive file id).
FILE_ID = "18S956r4jnHtSeT8z8t3z8AoJZjVnNqPJ"
WEIGHT_RELATIVE = Path("Gaze360") / "L2CSNet_gaze360.pkl"


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    model_dir = project_root / "models" / "l2cs"
    target = model_dir / WEIGHT_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        print(f"[skip] already exists: {target}")
        return

    try:
        import gdown
    except ImportError:
        print("Installing gdown...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown  # noqa: F401

    print(f"[download] L2CSNet_gaze360.pkl -> {target}")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "gdown",
            FILE_ID,
            "-O",
            str(target),
        ]
    )

    if not target.exists():
        raise FileNotFoundError(f"Download failed: {target}")

    print(f"\nDone. You can now run with model_path={target.relative_to(project_root).as_posix()}")


if __name__ == "__main__":
    main()
