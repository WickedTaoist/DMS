"""
Download OpenVINO head-pose model files (single canonical script).
"""

from pathlib import Path
from urllib.request import urlretrieve


BASE_URL = (
    "https://storage.openvinotoolkit.org/repositories/open_model_zoo/2022.3/models_bin/1/"
    "head-pose-estimation-adas-0001/FP16"
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    model_dir = project_root / "models" / "openvino"
    model_dir.mkdir(parents=True, exist_ok=True)

    targets = {
        "head_pose.xml": f"{BASE_URL}/head-pose-estimation-adas-0001.xml",
        "head_pose.bin": f"{BASE_URL}/head-pose-estimation-adas-0001.bin",
    }

    for local_name, url in targets.items():
        dst = model_dir / local_name
        print(f"[download] {url}")
        urlretrieve(url, dst)  # nosec B310 - trusted static source URL
        print(f"[ok] saved: {dst}")

    print("\nDone. You can now run with model_path=models/openvino/head_pose.xml")


if __name__ == "__main__":
    main()
