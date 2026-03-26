# Driver Phone Usage Detection (Research Prototype)

This project is a research-oriented computer vision prototype for detecting driver phone usage behavior in offline videos.

The core idea is not a single end-to-end classifier. Instead, it combines multiple visual evidence signals:

- head pose (downward tendency)
- gaze direction (downward or off-road)
- phone object detection
- hand-off-wheel detection

The system is designed for fast paper iteration: clear architecture, configurable experiments, and easy module extension.

## 1. Goals

- Support single-video and directory batch processing
- Produce results at three granularities:
  - frame-level
  - event-level
  - clip-level
- Export to JSON and CSV
- Keep architecture simple but extensible for:
  - fusion upgrades
  - VLM integration
  - new behavior categories

## 2. Architecture

Pipeline flow:

1. Video input
2. Decode and sample frames
3. Run multiple detectors per frame
4. Fuse evidence into risk score
5. Decide frame-level behavior label
6. Aggregate temporal events
7. Summarize clip-level statistics
8. Export JSON/CSV

Layer responsibilities:

- `detectors`: "what is observed"
- `fusion`: "how signals are combined"
- `decision`: "how behavior labels are determined"
- `aggregators`: "how frame labels become events"
- `runners`: "how experiments are executed"

## 3. Directory and File Guide

```text
driver_phone_usage/
├─ README.md
├─ requirements.txt
├─ pyproject.toml
├─ configs/
│  ├─ base.yaml
│  └─ experiments/
│     └─ exp_baseline.yaml
├─ src/
│  ├─ main.py
│  ├─ schemas/
│  │  ├─ common.py
│  │  ├─ frame_result.py
│  │  ├─ event_result.py
│  │  └─ clip_summary.py
│  ├─ detectors/
│  │  ├─ base_detector.py
│  │  ├─ registry.py
│  │  ├─ head_pose_detector.py
│  │  ├─ gaze_detector.py
│  │  ├─ phone_detector.py
│  │  ├─ hand_off_wheel_detector.py
│  │  └─ vlm_detector.py
│  ├─ fusion/
│  │  ├─ base_fuser.py
│  │  └─ rule_fuser.py
│  ├─ aggregators/
│  │  ├─ temporal_smoother.py
│  │  └─ event_aggregator.py
│  ├─ decision/
│  │  ├─ base_decider.py
│  │  ├─ threshold_policy.py
│  │  └─ rule_based_decider.py
│  ├─ pipelines/
│  │  ├─ frame_pipeline.py
│  │  └─ clip_pipeline.py
│  ├─ io/
│  │  ├─ video_reader.py
│  │  ├─ frame_sampler.py
│  │  └─ output_writer.py
│  ├─ runners/
│  │  ├─ run_single.py
│  │  ├─ run_batch.py
│  │  └─ experiment_runner.py
│  └─ utils/
│     ├─ config_loader.py
│     ├─ logger.py
│     ├─ time_utils.py
│     └─ id_utils.py
└─ outputs/
   ├─ json/
   ├─ csv/
   └─ logs/
```

### Root files

- `README.md`: project intro, architecture, usage, reproducibility
- `requirements.txt`: Python dependencies
- `pyproject.toml`: formatter/linter/project metadata

### Config files

- `configs/base.yaml`: default global config
- `configs/experiments/exp_baseline.yaml`: baseline experiment override

### Core source files

- `src/main.py`: command entrypoint
- `src/schemas/*`: structured data definitions for frame/event/clip
- `src/detectors/base_detector.py`: unified detector interface
- `src/detectors/registry.py`: detector plugin registry and builder
- `src/fusion/base_fuser.py`: fuser interface
- `src/fusion/rule_fuser.py`: simple explainable fusion
- `src/decision/base_decider.py`: decision interface
- `src/decision/rule_based_decider.py`: frame label decision by thresholds
- `src/aggregators/event_aggregator.py`: frame labels to continuous events
- `src/pipelines/frame_pipeline.py`: per-frame orchestration
- `src/pipelines/clip_pipeline.py`: full video orchestration
- `src/io/output_writer.py`: JSON/CSV export utilities
- `src/runners/*`: single, batch, experiment runs

## 4. Quick Start

### 4.1 Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4.2 Run single video

```bash
python -m src.main single --input path/to/video.mp4 --config configs/base.yaml
```

### 4.3 Run batch directory

```bash
python -m src.main batch --input_dir path/to/videos --config configs/base.yaml
```

### 4.4 Run baseline experiment

```bash
python -m src.main experiment --config configs/experiments/exp_baseline.yaml
```

## 5. Input/Output Schema

### Frame-level output

- frame metadata (`video_id`, `frame_index`, `timestamp_ms`)
- detector raw outputs
- fused evidence scores
- frame-level decision label

### Event-level output

- event id and type
- start/end frame and timestamp
- duration and evidence statistics

### Clip-level output

- total processed frames and duration
- event counts and duration ratio
- final clip risk score and clip label

## 6. How to Add a New Detector

1. Create detector class under `src/detectors/`
2. Inherit `BaseDetector`
3. Implement `setup()`, `infer()`, `teardown()`
4. Register it in `registry.py`
5. Add detector config in `configs/`

## 7. Experiment Reproducibility Notes

- Store model version in outputs
- Keep experiment config files immutable per run
- Save logs under `outputs/logs/`
- Use fixed frame sampling settings for fair comparisons

## 8. Current Scope and Future Work

Current scope:

- architecture skeleton
- rule-based fusion and decision baseline
- JSON/CSV export and batch experiment runner

Future work:

- learned fusion module
- VLM-assisted semantic reasoning
- additional risky behavior categories
