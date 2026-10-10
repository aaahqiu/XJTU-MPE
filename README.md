# XJTU-MPE dataset project page

XJTU-MPE 是西安交通大学的激光送丝定向能量沉积（LW-DED）熔池事件数据集。该仓库维护静态项目网页；原始数据和模型代码分别托管在 Hugging Face 和 EventDiff 仓库。

- 项目网页：[aaahqiu.github.io/XJTU-MPE](https://aaahqiu.github.io/XJTU-MPE/)
- 数据集与完整说明：[ahqiutkp/XJTU-MPE](https://huggingface.co/datasets/ahqiutkp/XJTU-MPE)
- 模型代码：[aaahqiu/EventDiff](https://github.com/aaahqiu/EventDiff)

## 页面内容

页面包含数据集介绍、作者与单位、60 次实验记录 / 当前公开 10 次 / 10 种功率条件 / 3 种模态的统计信息、可筛选的采集条件表、实验设备、真实记录的三种数据预览、下载与读取代码、文件字段说明、EventDiff 输入要求、临时 BibTeX 引用和公开联系方式。

2026-10-10 核对 Hugging Face 实际文件目录：每种条件目前仅发布编号 `1` 的记录，共 10 个记录、30 个数据文件，4,134,380,341 字节（约 4.13 GB）。数据集卡描述的 60 次是实验总量，网页分别显示实验总量与已公开数量；后续上传更多数据时应更新公开数量、文件大小和核对日期。

网页沿用原项目页的英文与蓝色学术风格，改用独立 CSS，无前端框架、构建步骤或 CDN 依赖。支持手机布局、键盘操作、标签页切换、代码复制和返回顶部。下载链接和核心内容在关闭 JavaScript 时仍可使用。

## 本地预览

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8000>。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `index.html` | 页面内容、数据与代码入口、下载和读取示例、引用 |
| `static/css/dataset.css` | 页面全部样式与响应式布局 |
| `static/js/index.js` | 条件筛选、无障碍标签页、复制、返回顶部 |
| `static/images/*-preview.png` | 从真实 `900W/1` 记录生成的三种预览图 |
| `static/images/preview-provenance.json` | 图像来源、采样方式、文件哈希和统计信息 |
| `scripts/generate_previews.py` | 预览图生成脚本（仅维护时使用） |
| `DATASET_CARD.md` | 已核对的数据摘要、使用方法和重要限制 |

模板自带的其他 CSS/JS 保留在仓库内，当前页面不加载这些资源。

## 重新生成真实预览

需要 Python、NumPy、pandas 和 matplotlib；这些依赖只用于维护预览图，部署网站不需要安装它们。

准备一个本地目录，包含以下来自 `data/900W/1/` 的文件：

- `para.csv`：完整参数文件。
- `3dscan.asc`：完整扫描文件。
- `event-slice.csv`：`event.csv` 的字节范围 `90000000–91799999`（含端点）。脚本丢弃两端不完整的行，取首个完整事件开始的 10 ms 窗口。

```bash
python scripts/generate_previews.py /path/to/downloaded-preview-data
```

脚本输出 PNG 和来源 JSON 到 `static/images/`。默认复现当前页面的 900 W 样例；若更换记录或采样窗口，应同步更新网页图片说明和来源记录。不要将原始大体积数据提交到此网页仓库。

## GitHub Pages

使用现有 GitHub Pages：`main` 分支、根目录 `/`，保留 `.nojekyll`。推送页面修改后自动更新 <https://aaahqiu.github.io/XJTU-MPE/>。

## 数据与实现的关系

Hugging Face 发布 `event.csv`、`para.csv`、`3dscan.asc`。EventDiff 训练使用 `voxel_grid.npy` 和 `laser_power_per_frame.npy`，默认还需要 EventVAE 权重。应先按研究设置预处理原始数据，不应将 CSV/ASC 直接传入模型训练入口。`main` 分支维护核心训练与评估；`exp` 分支维护论文实验。

引用暂用数据集卡提供的 `@unpublished{tan2026processconditioned}`；论文正式出版后再更新 venue、DOI 与论文链接。

## 致谢与许可证

项目页改编自 [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) 和 [Nerfies](https://nerfies.github.io/)，保留原模板署名；网页模板采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。

数据集的 Hugging Face 元数据当前标记为 MIT。网页模板许可证与数据集许可证分别适用；数据集许可信息以 [Hugging Face 数据集卡](https://huggingface.co/datasets/ahqiutkp/XJTU-MPE) 为准。
