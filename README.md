# Driver Phone Usage Detection
# 驾驶员玩手机行为检测科研原型

## 1. What This Project Is
## 1. 这个项目是什么

**中文**  
这是一个面向论文实验的计算机视觉科研原型项目，目标是从离线视频中分析驾驶员是否存在“玩手机”行为。  
当前系统不是“一个模型直接输出最终答案”的端到端分类器，而是一个多证据分析框架：

- 头部下倾信号
- 视线下移信号
- 手机目标检测信号
- 手离方向盘信号

这些信号先分别由 detector 输出，再经过融合、判定、事件聚合，最终得到帧级、事件级和视频级结果。

**English**  
This repository is a research-oriented computer vision prototype for offline driver phone-use analysis.  
The current system is not a single end-to-end classifier. Instead, it is a multi-evidence analysis framework:

- head-down signal
- downward-gaze signal
- phone detection signal
- hand-off-wheel signal

Each signal is first produced by a detector, then passed through fusion, decision, and event aggregation, finally producing frame-level, event-level, and clip-level results.

---

## 2. What It Can Do Now
## 2. 目前已经能做什么

**中文**  
基于当前代码，项目已经可以完成一个完整的最小可运行流程：

1. 从单个视频或 `data/video` 批量读取视频  
2. 使用 OpenCV 解码视频并按固定 FPS 抽帧  
3. 逐帧调用多个 detector（当前是 mock / dummy 实现）  
4. 使用规则融合器生成 `risk_score`  
5. 使用规则判定器生成帧级标签  
6. 将连续可疑帧聚合为事件段  
7. 生成视频级 `clip_summary`  
8. 导出 JSON / CSV  
9. 批量运行时自动生成 `batch_summary.csv`

**English**  
With the current codebase, the project can already run a complete minimal pipeline:

1. Read either one video or a batch of videos from `data/video`
2. Decode videos with OpenCV and sample frames at a fixed FPS
3. Run multiple detectors per frame (currently mock / dummy implementations)
4. Produce a `risk_score` through a rule-based fuser
5. Produce frame-level labels through a rule-based decider
6. Aggregate consecutive suspicious frames into event segments
7. Generate a clip-level summary
8. Export JSON / CSV
9. Generate `batch_summary.csv` automatically in batch mode

---

## 3. What It Cannot Do Yet
## 3. 目前还不能做什么

**中文**  
当前项目仍然是“科研骨架 + 可运行 pipeline”，还没有完成以下核心能力：

- 还没有接入真实 OpenVINO 头姿模型
- 还没有接入真实 OpenVINO 视线模型
- 还没有接入真实 YOLO 手机检测模型
- 还没有接入真实手离方向盘检测逻辑
- 当前 detector 输出主要是固定值或空结果
- 当前 fusion 是可解释 baseline，不是学习型融合
- 当前没有接入 VLM 推理
- 当前没有完整评估模块、可视化模块、单元测试模块

**English**  
The current project is still a “research skeleton + runnable pipeline”.  
The following capabilities are not finished yet:

- no real OpenVINO head-pose model integration yet
- no real OpenVINO gaze model integration yet
- no real YOLO phone detector integration yet
- no real hand-off-wheel logic yet
- detector outputs are still fixed values or empty placeholders
- the current fusion is a simple interpretable baseline, not a learned fusion module
- no VLM reasoning module yet
- no complete evaluation, visualization, or unit testing modules yet

---

## 4. Core Design Idea
## 4. 核心设计思想

**中文**  
项目采用的是一种非常适合论文实验迭代的架构：

- 面向对象：每个 detector、fuser、decider 都有统一接口
- Pipeline 编排：整条链路按固定顺序运行
- 插件化 detector：未来接新模型时不需要重写主流程
- 独立事件层：让 frame-level 结果可以被聚合成 event-level
- 独立 clip summary：方便论文做视频级统计

你可以把这个项目理解成：

`视频读取层 -> 感知层 -> 融合层 -> 判定层 -> 时序聚合层 -> 导出层`

**English**  
The project uses an architecture that is very suitable for iterative academic experiments:

- object-oriented design: detectors, fusers, and deciders share unified interfaces
- pipeline orchestration: the whole flow runs in a fixed sequence
- plugin-based detectors: new models can be integrated without rewriting the main flow
- independent event layer: frame-level outputs can be aggregated into event-level segments
- independent clip summary: convenient for video-level reporting in research papers

You can understand the project as:

`video I/O -> perception -> fusion -> decision -> temporal aggregation -> export`

---

## 5. End-to-End Execution Flow
## 5. 端到端执行流程

### Batch mode / 批量模式

执行命令：

```bash
python -m src.main batch --config configs/base.yaml
```

实际执行顺序如下：

1. `src/main.py`  
   解析命令行，读取配置，初始化日志。

2. `src/runners/run_batch.py`  
   从配置中读取 `data.video_dir` 和 `data.video_glob`，扫描所有视频。

3. `src/runners/run_single.py`  
   对每个视频初始化 detector、fuser、decider，并调用 `ClipPipeline`。

4. `src/pipelines/clip_pipeline.py`  
   逐帧处理整个视频，随后执行标签平滑、事件聚合和 clip 汇总。

5. `src/pipelines/frame_pipeline.py`  
   对每一帧完成 detector -> fusion -> decision。

6. `src/io/output_writer.py`  
   写出每视频 JSON / CSV，并由 batch runner 写出 `batch_summary.csv`。

**English**  
The actual execution order in batch mode is:

1. `src/main.py`  
   Parse CLI arguments, load config, initialize logging.

2. `src/runners/run_batch.py`  
   Read `data.video_dir` and `data.video_glob` from config, then scan all videos.

3. `src/runners/run_single.py`  
   For each video, initialize detectors, fuser, decider, and call `ClipPipeline`.

4. `src/pipelines/clip_pipeline.py`  
   Process the whole video frame by frame, then run smoothing, event aggregation, and clip summary generation.

5. `src/pipelines/frame_pipeline.py`  
   For each frame, run detector -> fusion -> decision.

6. `src/io/output_writer.py`  
   Write per-video JSON / CSV outputs, and the batch runner writes `batch_summary.csv`.

---

## 6. Code Structure for Beginners
## 6. 给新手看的代码结构说明

下面这一节是按“你第一次阅读代码时最容易理解”的顺序来写的。

This section is organized in a beginner-friendly reading order.

### 6.1 Root files / 根目录文件

- `README.md`  
  中文：项目说明文档。  
  English: project documentation.

- `requirements.txt`  
  中文：运行依赖。  
  English: runtime dependencies.

- `pyproject.toml`  
  中文：Python 工程配置，例如格式化和 lint 工具参数。  
  English: Python project configuration for formatting and linting tools.

### 6.2 Config files / 配置文件

- `configs/base.yaml`  
  中文：全局基础配置，控制输入目录、输出目录、抽帧率、detector 启用情况、融合权重、判定阈值、日志等级。  
  English: global base config controlling input/output directories, sampling FPS, enabled detectors, fusion weights, decision thresholds, and logging level.

- `configs/experiments/exp_baseline.yaml`  
  中文：在基础配置上做实验级覆盖。  
  English: experiment-level override on top of the base config.

- `configs/detectors/*.yaml`  
  中文：每个 detector 的私有参数。  
  English: private parameters for each detector.

- `configs/decision/rule_based.yaml`  
  中文：规则判定相关参数。  
  English: parameters for rule-based decision logic.

### 6.3 `src/` source tree / `src/` 源码目录

```text
src/
├─ main.py
├─ schemas/
├─ detectors/
├─ fusion/
├─ decision/
├─ aggregators/
├─ pipelines/
├─ io/
├─ runners/
└─ utils/
```

#### `src/main.py`

**中文**：命令行总入口。  
**English**: top-level CLI entrypoint.

作用：
- 解析 `single / batch / experiment`
- 加载 YAML 配置
- 初始化日志
- 调度对应 runner

#### `src/schemas/`

**中文**：定义系统中最重要的数据结构。  
**English**: defines the key data structures shared across the system.

- `common.py`  
  定义 `FrameMeta`、`BBox`、`DetectorOutput`

- `frame_result.py`  
  定义每一帧处理后的完整结果结构

- `event_result.py`  
  定义连续事件段结构

- `clip_summary.py`  
  定义整段视频的汇总结构

#### `src/detectors/`

**中文**：感知层，每个 detector 只负责“从一帧里看出某种信号”。  
**English**: perception layer; each detector extracts one type of signal from a frame.

- `base_detector.py`  
  detector 抽象接口，定义 `setup / infer / teardown`

- `registry.py`  
  根据配置动态构建 detector 列表

- `head_pose_detector.py`  
  头姿 detector 占位实现

- `gaze_detector.py`  
  视线 detector 占位实现

- `phone_detector.py`  
  手机 detector 占位实现

- `hand_off_wheel_detector.py`  
  手离方向盘 detector 占位实现

- `vlm_detector.py`  
  为未来 VLM 预留的 detector 接口

#### `src/fusion/`

**中文**：把多个 detector 输出转换成统一风险分数。  
**English**: turns multiple detector outputs into a unified risk score.

- `base_fuser.py`  
  融合器接口

- `rule_fuser.py`  
  当前 baseline 融合器，采用加权和

#### `src/decision/`

**中文**：根据融合结果生成最终帧级标签。  
**English**: converts fusion outputs into final frame-level labels.

- `base_decider.py`  
  判定器接口

- `rule_based_decider.py`  
  当前使用的规则阈值判定器

- `threshold_policy.py`  
  用于表达判定阈值的数据结构

#### `src/aggregators/`

**中文**：处理时间维度，把帧级结果变成事件级结果。  
**English**: handles the temporal dimension, turning frame-level results into event-level segments.

- `temporal_smoother.py`  
  对帧标签做简单时间平滑

- `event_aggregator.py`  
  将连续 `suspected_phone_use` 帧聚合为事件

#### `src/pipelines/`

**中文**：系统编排层。  
**English**: orchestration layer.

- `frame_pipeline.py`  
  负责单帧处理

- `clip_pipeline.py`  
  负责整段视频处理

#### `src/io/`

**中文**：输入输出层。  
**English**: input/output layer.

- `video_reader.py`  
  OpenCV 视频解码与视频列表扫描

- `frame_sampler.py`  
  固定 FPS 抽帧，并构造 `FrameContext`

- `output_writer.py`  
  导出 JSON / CSV

#### `src/runners/`

**中文**：运行调度层。  
**English**: execution runners.

- `run_single.py`  
  单视频完整处理

- `run_batch.py`  
  批量处理所有视频并生成 `batch_summary.csv`

- `experiment_runner.py`  
  按实验配置切换 single / batch

#### `src/utils/`

**中文**：基础辅助模块。  
**English**: low-level support modules.

- `config_loader.py`  
  配置读取与继承合并

- `logger.py`  
  统一日志

- `path_utils.py`  
  相对路径解析与目录检查

- `time_utils.py`  
  帧号与时间换算

- `id_utils.py`  
  事件 ID 生成

- `video_name_parser.py`  
  从文件名解析实验标签

---

## 7. What Each Major Stage Produces
## 7. 每个阶段会产生什么结果

### Frame-level / 帧级

每一帧都会得到：
- 帧元信息
- detector 原始输出
- `risk_score`
- 帧级标签 `normal` 或 `suspected_phone_use`

Each frame produces:
- frame metadata
- raw detector outputs
- `risk_score`
- a frame label: `normal` or `suspected_phone_use`

### Event-level / 事件级

把连续的可疑帧合并为一个 event，主要字段包括：
- `start_frame`
- `end_frame`
- `duration_frames`
- `duration_ms`
- `max_risk_score`

Consecutive suspicious frames are merged into one event, with fields such as:
- `start_frame`
- `end_frame`
- `duration_frames`
- `duration_ms`
- `max_risk_score`

### Clip-level / 视频级

整段视频会得到一个 `clip_summary`，主要包括：
- 总处理帧数
- 事件数量
- 总事件时长
- 风险分数
- 视频级标签

Each whole video produces one `clip_summary`, mainly including:
- total processed frames
- number of events
- total event duration
- risk score
- clip-level label

---

## 8. Current Output Structure
## 8. 当前输出目录结构

### Per-video outputs / 每视频输出

- `outputs/json/<video_stem>/frame_results.json`
- `outputs/json/<video_stem>/events.json`
- `outputs/json/<video_stem>/clip_summary.json`
- `outputs/csv/<video_stem>/frame_results.csv`
- `outputs/csv/<video_stem>/events.csv`
- `outputs/csv/<video_stem>/clip_summary.csv`

### Batch-level outputs / 批量输出

- `outputs/csv/batch_summary.csv`
- `outputs/logs/run.log`
- `outputs/logs/run_batch.log`

### `batch_summary.csv`

当前至少包含以下字段：

- `video_id`
- `file_name`
- `file_path`
- `parsed_label`
- `total_frames`
- `processed_frames`
- `duration_sec`
- `num_events`
- `total_event_duration_sec`
- `max_risk_score`
- `clip_label`
- `output_json_path`
- `output_csv_path`
- `status`
- `error_message`

This table currently contains at least:

- `video_id`
- `file_name`
- `file_path`
- `parsed_label`
- `total_frames`
- `processed_frames`
- `duration_sec`
- `num_events`
- `total_event_duration_sec`
- `max_risk_score`
- `clip_label`
- `output_json_path`
- `output_csv_path`
- `status`
- `error_message`

---

## 9. How a Beginner Should Read the Code
## 9. 新手建议按什么顺序读代码

建议阅读顺序：

1. `README.md`
2. `configs/base.yaml`
3. `src/main.py`
4. `src/runners/run_batch.py`
5. `src/runners/run_single.py`
6. `src/pipelines/clip_pipeline.py`
7. `src/pipelines/frame_pipeline.py`
8. `src/detectors/base_detector.py`
9. `src/fusion/rule_fuser.py`
10. `src/decision/rule_based_decider.py`
11. `src/aggregators/event_aggregator.py`
12. `src/io/output_writer.py`

Recommended reading order:

1. `README.md`
2. `configs/base.yaml`
3. `src/main.py`
4. `src/runners/run_batch.py`
5. `src/runners/run_single.py`
6. `src/pipelines/clip_pipeline.py`
7. `src/pipelines/frame_pipeline.py`
8. `src/detectors/base_detector.py`
9. `src/fusion/rule_fuser.py`
10. `src/decision/rule_based_decider.py`
11. `src/aggregators/event_aggregator.py`
12. `src/io/output_writer.py`

---

## 10. How to Run the Project
## 10. 如何运行项目

### Install / 安装

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Download OpenVINO head-pose model / 下载 OpenVINO 头姿模型

```bash
python scripts/download_openvino_head_pose.py
```

### Run one video / 运行单个视频

```bash
python -m src.main single --input path/to/video.mp4 --config configs/base.yaml
```

### Run all videos in `data/video` / 运行 `data/video` 下全部视频

```bash
python -m src.main batch --config configs/base.yaml
```

### Override input directory / 临时覆盖输入目录

```bash
python -m src.main batch --input_dir path/to/other_videos --config configs/base.yaml
```

---

## 11. Current Design Choices
## 11. 当前设计为什么这么做

**中文**
- 用 `BaseDetector` 做统一接口，是为了后续接真实模型时不动主流程
- 用 `FramePipeline` 和 `ClipPipeline` 分层，是为了让单帧逻辑和整视频逻辑解耦
- 用 `rule_fuser` 和 `rule_based_decider`，是为了先建立可解释 baseline
- 用 `event_aggregator`，是为了支持论文中的时序事件统计
- 用 `batch_summary.csv`，是为了让实验结果可直接进入统计分析

**English**
- `BaseDetector` provides a stable contract so real models can be added without changing the main pipeline
- `FramePipeline` and `ClipPipeline` separate per-frame logic from whole-video logic
- `rule_fuser` and `rule_based_decider` provide an interpretable baseline
- `event_aggregator` supports temporal event statistics for research papers
- `batch_summary.csv` makes experiment outputs directly usable for downstream analysis

---

## 12. Planned Next Steps
## 12. 后续待完成功能

### Near-term / 近期

- integrate real OpenVINO gaze model  
- integrate real YOLO phone detector  
- implement real hand-off-wheel detector  
- enrich `batch_summary.csv` with more experiment metadata  

### Mid-term / 中期

- support stronger fusion strategies  
- support VLM-based semantic reasoning  
- support more behavior categories  
- add visualization and evaluation scripts  

### Long-term / 长期

- build a more complete experiment/evaluation framework  
- compare multiple detector combinations and fusion strategies  
- connect the prototype more directly to paper-ready metrics and figures  

---

## 13. Important Reminder
## 13. 一个重要提醒

**中文**  
当前项目最重要的价值，不是“检测精度已经完成”，而是：  
**工程骨架已经稳定，实验数据流已经打通，后续接真实模型时不需要推翻重来。**

**English**  
The most important value of the current project is not that detection accuracy is already finished.  
It is that **the engineering skeleton is now stable, the experiment data flow is already connected end-to-end, and real models can be integrated later without rewriting the whole project.**
