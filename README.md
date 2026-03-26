# Driver Phone Usage Detection / 驾驶员玩手机检测（科研原型）

## 1. Project Overview / 项目概述

**EN**: This repository is a research prototype for offline driver phone-use analysis. It combines multiple visual signals instead of relying on one end-to-end classifier.  
**ZH**：本仓库是一个离线视频科研原型，用于检测驾驶员玩手机行为。系统通过多证据联合判断，而非单一端到端分类器。

Main evidence signals / 主要证据信号：
- Head pose (downward trend) / 头部下倾
- Gaze direction (downward or off-road) / 视线下移或偏离前方
- Phone detection / 手机目标检测
- Hand-off-wheel signal / 手离方向盘信号

---

## 2. Architecture / 系统架构

Pipeline / 流程：
1. Video input / 视频输入
2. Decode + frame sampling / 解码与抽帧
3. Multi-detector inference / 多检测器推理
4. Evidence fusion / 证据融合
5. Frame-level decision / 帧级判定
6. Event aggregation / 事件聚合
7. Clip summary / 片段级汇总
8. JSON/CSV export / 结构化导出

Layer roles / 分层职责：
- `detectors`: raw signal extraction / 原始信号提取
- `fusion`: risk score calculation / 风险分数融合
- `decision`: frame label generation / 帧级标签生成
- `aggregators`: temporal event construction / 时序事件构建
- `runners`: single and batch orchestration / 单视频与批量调度

---

## 3. Directory Guide / 目录说明

```text
driver_phone_usage/
├─ README.md
├─ requirements.txt
├─ pyproject.toml
├─ configs/
│  ├─ base.yaml
│  └─ experiments/
│     └─ exp_baseline.yaml
├─ data/
│  └─ video/                      # batch input directory
├─ src/
│  ├─ main.py
│  ├─ schemas/
│  ├─ detectors/
│  ├─ fusion/
│  ├─ decision/
│  ├─ aggregators/
│  ├─ pipelines/
│  ├─ io/
│  ├─ runners/
│  └─ utils/
└─ outputs/
   ├─ json/
   ├─ csv/
   └─ logs/
```

Key files / 核心文件：
- `src/main.py`: CLI entry / 命令行入口
- `src/runners/run_batch.py`: batch runner + batch summary / 批量运行与汇总
- `src/pipelines/clip_pipeline.py`: end-to-end clip pipeline / 视频端到端流程
- `src/io/output_writer.py`: JSON/CSV writer / 结果导出
- `src/utils/video_name_parser.py`: filename metadata parsing / 文件名标签解析

---

## 4. Configuration / 配置说明

`configs/base.yaml` (important keys / 关键字段):

- `data.video_dir`: default batch video directory (default `data/video`)
- `data.video_glob`: video match pattern (default `*.mp4`)
- `output.root_dir`: output root directory (default `outputs`)
- `pipeline.sampling_fps`: target sampling fps
- `detectors.enabled`: enabled detector plugins
- `logging.level`: logging level

Path rule / 路径规则：
- Relative paths are resolved against project root.
- 相对路径统一相对于项目根目录解析。

---

## 5. Quick Start / 快速开始

### 5.1 Install / 安装依赖

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 5.2 Run single video / 单视频运行

```bash
python -m src.main single --input path/to/video.mp4 --config configs/base.yaml
```

### 5.3 Run batch (default from `data/video`) / 批量运行（默认读取 `data/video`）

```bash
python -m src.main batch --config configs/base.yaml
```

Optional override / 可选覆盖目录：

```bash
python -m src.main batch --input_dir path/to/other_videos --config configs/base.yaml
```

---

## 6. Output Structure / 输出结构

Per-video output / 每视频输出：
- `outputs/json/<video_stem>/clip_summary.json`
- `outputs/json/<video_stem>/events.json`
- `outputs/json/<video_stem>/frame_results.json`
- `outputs/csv/<video_stem>/frame_results.csv`
- `outputs/csv/<video_stem>/events.csv`
- `outputs/csv/<video_stem>/clip_summary.csv`

Batch-level output / 批量汇总输出：
- `outputs/csv/batch_summary.csv`
- `outputs/logs/run_batch.log`

`batch_summary.csv` fields / 字段（用于论文统计）：
- `video_id`, `file_name`, `file_path`, `parsed_label`
- `total_frames`, `processed_frames`, `duration_sec`
- `num_events`, `total_event_duration_sec`
- `max_risk_score`, `clip_label`
- `output_json_path`, `output_csv_path`

---

## 7. Add New Detector / 新增检测器

1. Create a class in `src/detectors/` / 在 `src/detectors/` 新建类  
2. Inherit `BaseDetector` / 继承 `BaseDetector`  
3. Implement `setup()`, `infer()`, `teardown()` / 实现三个标准方法  
4. Register in `src/detectors/registry.py` / 注册到 registry  
5. Add config entries in `configs/base.yaml` / 补充配置项  

---

## 8. Reproducibility Notes / 复现实验建议

- Keep config snapshots for each run / 每次实验保留配置快照
- Record model versions in outputs / 在输出中记录模型版本
- Keep deterministic sampling settings / 固定抽帧参数保证可比性
- Use `batch_summary.csv` as primary analysis table / 以 `batch_summary.csv` 作为论文统计主表
