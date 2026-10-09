# XJTU-MPE

**XJTU-MPE** 是一个 LWDED 熔池事件数据集。本仓库提供数据集项目页和发布文档的初版。

> 当前状态：项目页初版。数据文件、样本量、事件类别、作者、下载链接及数据集许可证尚待补充。

## 页面内容

- 数据集简介（Overview）
- 数据规格（Dataset）
- 熔池事件样例（Samples，待补充）
- 数据下载与文档入口（Access）
- 正式引用信息（Citation，待补充）

页面沿用 Academic Project Page Template 的学术页面布局，支持桌面和手机浏览。未确认的信息明确标注为待发布，下载按钮在提供真实链接前保持禁用。

## 本地预览

在仓库根目录运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

然后打开 <http://127.0.0.1:8000>。这是静态网页，无需安装前端依赖或构建。

## 修改内容

| 文件 | 用途 |
| --- | --- |
| `index.html` | 数据集名称、简介、作者、统计信息、样例、下载链接和引用 |
| `static/css/dataset.css` | 数据集页面的补充样式与移动端布局 |
| `static/css/index.css` | 原模板基础样式 |
| `static/js/index.js` | 返回顶部交互 |
| `static/images/dataset-icon.svg` | 项目页面图标 |
| `DATASET_CARD.md` | 数据集说明与发布准备清单 |

样例图片或视频可放到 `static/images/` 或 `static/videos/`，再替换页面中的样例占位区域。大体积数据文件应使用独立的数据托管服务或下载地址；本仓库当前只包含项目页与文档。

## GitHub Pages

仓库包含 `.nojekyll`，可直接作为 GitHub Pages 静态站点。上传后，在仓库的 **Settings → Pages** 中选择 **Deploy from a branch**，分支选 `main`，目录选 `/ (root)`。

按上述方式启用后，预期页面地址为 <https://aaahqiu.github.io/XJTU-MPE/>。

## 发布前待补充

- [ ] 作者、单位与联系方式
- [ ] 研究背景和适用任务
- [ ] 数据采集方式、文件格式和目录结构
- [ ] 事件类别、标注规范、样本量和数据划分
- [ ] 真实样例与下载链接
- [ ] 数据集许可证和使用条件
- [ ] 正式引用 / BibTeX

## 致谢与许可证

项目页基于 [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template)，其部分设计来自 [Nerfies](https://nerfies.github.io/)。保留原模板署名；网站模板采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可证。

**网站模板的许可证不代表数据集许可证。** XJTU-MPE 数据集的许可证将在正式发布前另行公布。
