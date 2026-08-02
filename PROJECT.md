# PROJECT.md —— 项目交接文档（Quest ↔ chat 协作台账）

> 本文件是"项目经理（Quest）"与"同事（chat/编辑器助手）"之间的交接媒介。
> 规则：Quest 负责规划与汇报；chat 负责执行并更新"当前进度"；两边都只通过本文件沟通。

## 一、项目目标

- 项目名称：广州天气数据可视化看板
- 目标：部署在 GitHub Pages 上的广州天气可视化网站，每天自动更新数据
- 数据源：Open-Meteo 免费天气 API（无需注册、无需 API Key）
- 技术栈：Python 3（requests）+ Chart.js（CDN）+ GitHub Pages + GitHub Actions

## 二、当前进度

- [x] fetch_weather.py：数据获取脚本，已创建，本地运行验证通过（成功生成 guangzhou_weather.json，7 天数据）
- [x] guangzhou_weather.json：已生成，结构符合要求（city / updated_at / data）
- [x] index.html：Chart.js 折线图页面，已创建，本地服务器验证通过（HTTP 200）
- [x] .github/workflows/daily_update.yml：每日自动更新工作流，已创建（每天 UTC 0 点 = 北京时间早 8 点，支持手动触发）
- [ ] 部署到 GitHub Pages（待办）
- [ ] 本地代码提交到 GitHub 仓库（待办）

## 三、待办问题 / 下一步任务

1. 将项目文件提交到 GitHub 仓库（git init → add → commit → push）
2. 在 GitHub 仓库 Settings → Pages 启用 GitHub Pages（main 分支根目录）
3. 验证 Actions 自动更新和网页访问

## 四、问题记录

- （暂无）

## 五、交接记录

- 2026-08-02：Quest 与 chat 建立交接机制；chat 完成项目三件套（脚本/网页/工作流）并验证通过。
