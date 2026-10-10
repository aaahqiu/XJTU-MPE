# XJTU-MPE Dataset Card

本文件是项目页的数据摘要，2026-10-10 根据 [Hugging Face 数据集卡](https://huggingface.co/datasets/ahqiutkp/XJTU-MPE/blob/main/README.md) 和 [EventDiff README](https://github.com/aaahqiu/EventDiff/blob/main/README.md) 核对。完整说明及后续更新以对应源仓库为准。

## 数据概览

XJTU-MPE 包含西安交通大学激光送丝定向能量沉积（LW-DED）实验的事件相机观测、对齐工艺参数和沉积轨迹三维扫描，用于研究熔池动态、工艺条件驱动的事件预测，以及在线观测与沉积几何的关系。

| 项目 | 内容 |
| --- | --- |
| 实验中的独立单道记录 | 60（数据集卡描述的实验总量） |
| 当前实际公开记录 | 10，每条件仅编号 `1`（2026-10-10 文件目录核对） |
| 当前公开文件大小 | 30 个数据文件，4,134,380,341 字节，约 4.13 GB |
| 激光功率条件 | 10，每条件 6 次重复 |
| 恒定功率记录 | 24 |
| 变化功率记录 | 36 |
| 数据模态 | 事件流、工艺参数、沉积轨迹点云 |
| 事件相机 | Prophesee EVK4 HD / Sony IMX636，1280 × 720 像素 |
| 工艺参数采样 | Beckhoff 控制器，500 Hz |
| 材料 | 304 不锈钢丝，直径 0.8 mm；Q235 基板 |
| 名义速度 | 沉积运动 12 mm/s；送丝 15 mm/s |
| 三维扫描仪 | Creality Raptor Pro |
| 数据托管 | [Hugging Face](https://huggingface.co/datasets/ahqiutkp/XJTU-MPE) |
| 数据集许可 | Hugging Face 元数据标记为 MIT |

作者：Kunpeng Tan、Ao Yang、Huaqing Zhang、Runze Yuan、Chenxi Wang、Xingwu Zhang、Zhibin Zhao。

单位：西安交通大学机械工程学院，装备运行安全与智能监控国家地方联合工程研究中心。通讯作者：Zhibin Zhao，`zhaozhibin@xjtu.edu.cn`。

## 功率条件

| 目录 | 功率变化（总功率，W） | 记录数 |
| --- | --- | ---: |
| `900W` | 900 → 900 | 6 |
| `1000W` | 1000 → 1000 | 6 |
| `1100W` | 1100 → 1100 | 6 |
| `1200W` | 1200 → 1200 | 6 |
| `900-1100W` | 900 → 1100 | 6 |
| `900-1200W` | 900 → 1200 | 6 |
| `1000-1200W` | 1000 → 1200 | 6 |
| `1100-900W` | 1100 → 900 | 6 |
| `1200-900W` | 1200 → 900 | 6 |
| `1200-1000W` | 1200 → 1000 | 6 |

目录名表示名义总功率；`900-1200W` 指一次记录中的 900 W → 1200 W 转变。激光启停是研究中的瞬态阶段，不是独立采集目录。记录编号在各条件内独立，不表示训练 / 验证 / 测试划分。

表中记录数是数据集卡描述的实验数量。2026-10-10 通过 Hugging Face 文件树 API 核对，目前每个条件目录仅有 `1/`，共 10 个可下载记录。不要将 60 次实验总量表述为当前可下载数量；实际发布范围以 Hugging Face 文件目录为准。

## 文件结构与读取

```text
data/<condition>/<recording_id>/
├── event.csv
├── para.csv
└── 3dscan.asc
```

以 `(condition, recording_id)` 唯一标识一个记录。

- `event.csv`：表头 `t,x,y,p`；时间戳单位 µs，像素坐标，极性 0/1。有符号极性为 −1/+1，转换前先转为有符号整数，防止无符号下溢。数据集卡说明保留原始坐标与时间戳，未转为模型体素。
- `para.csv`：UTF-8 BOM；第一行字段名，第二行源类型标签，数值读取应跳过第二行。字段为 `timestamp,laser_power,feed_rate,material_rate,vx,vy,vz`。部分值为小数，不应根据 INT32 元数据强制整型。`laser_power × 6` 得到目录名所用的总功率。
- `3dscan.asc`：无表头的空白分隔文本。前三列为 XYZ，其他列为保留的扫描属性。扫描不是每个事件的高度标签；高度计算需要基板参考平面、轨迹方向提取和时间轴上的空间配准。

```python
from pathlib import Path
import numpy as np
import pandas as pd

root = Path("XJTU-MPE/data/900W/1")
events = pd.read_csv(root / "event.csv", nrows=100_000)
events["p_signed"] = events["p"].astype("int8") * 2 - 1
params = pd.read_csv(root / "para.csv", encoding="utf-8-sig", skiprows=[1])
params["power_total_W"] = params["laser_power"] * 6
xyz = np.loadtxt(root / "3dscan.asc", usecols=(0, 1, 2))
```

事件 CSV 较大，可使用 pandas `chunksize` 分块读取。

## 时间对齐

工艺时间戳被平移到不变的事件相机时间轴，以首次激光激活与事件密度估计的起始点进行对齐，直方图 bin 为 2,000 µs。这是起始点对齐，不代表硬件触发级同步精度。参数保留原始样本，没有插值或时间裁剪。时间零点不一定是沉积开始，不应跨记录比较绝对时间戳。

## EventDiff 输入

[EventDiff](https://github.com/aaahqiu/EventDiff) 使用事件历史和激光功率条件预测未来事件序列。每个记录目录应包含 `voxel_grid.npy` 与 `laser_power_per_frame.npy`，默认 latent codec 需要 EventVAE 权重。因此原始 CSV/ASC 数据需要预处理后才能用于训练。模型权重、缓存 latent 与生成结果不在代码仓库内。

`main` 分支：核心训练、逐 epoch 验证、模型选择、测试评估。`exp` 分支：论文实验、基线、消融和报告工具。

## 项目页预览来源

网页展示真实 `900W/1` 记录。事件图来自 `event.csv` 的有限字节片段，累积 20.460428–20.470428 s 的 16,740 个事件。功率曲线使用全部 16,801 个参数样本，并将控制器功率乘以 6。扫描图对 816,525 个点每 40 个保留一个，显示原始 XYZ 和 z 坐标颜色，没有进行高度基准拟合。

预览生成脚本：`scripts/generate_previews.py`。来源、SHA-256、采样方式记录在 `static/images/preview-provenance.json`。原始大文件不包含在此网页仓库内。

## 引用

数据集卡提供的临时 manuscript 引用；venue、DOI 与公开论文链接尚未提供。

```bibtex
@unpublished{tan2026processconditioned,
  title = {Process-Conditioned Diffusion for Forecasting Melt-Pool Dynamics via Event-based Sensing in Laser Wire Directed Energy Deposition},
  author = {Tan, Kunpeng and Yang, Ao and Zhang, Huaqing and Yuan, Runze and Wang, Chenxi and Zhang, Xingwu and Zhao, Zhibin},
  year = {2026},
  note = {Manuscript}
}
```

## 更新记录

- 2026-10-10：核对已发布数据与代码，更新网页、文档、真实预览和引用。
- 2026-10-09：创建项目页初版。
