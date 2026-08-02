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
- [x] 本地 git 仓库初始化并提交（分支 main）
- [x] 推送到 GitHub 远程仓库（https://github.com/2108993924-ctrl/guangzhou-weather）
- [x] GitHub Pages 已启用并部署成功
- [x] 网站访问验证通过：https://2108993924-ctrl.github.io/guangzhou-weather/（HTTP 200）
- [x] Actions 自动更新工作流手动触发测试通过（success，数据已自动更新并重新部署）

## 三、待办问题 / 下一步任务

1. 观察每日定时更新是否按预期运行（预计每天北京时间 8 点）
2. （可选）后续可扩展：降雨量柱状图、更长时间预报、城市切换等

## 四、问题记录

- 已解决：首次查询 GitHub Pages API 返回 404，原因系 Pages 配置刚保存未生效，稍后部署完成即恢复正常
- 已解决：PowerShell 中 curl 参数与 Invoke-WebRequest 冲突，改用 curl.exe
- 已解决：.aicoding-chat-workspace 为文件而非目录，.gitignore 改用不带斜杠写法成功忽略

## 五、交接记录

- 2026-08-02：Quest 与 chat 建立交接机制；chat 完成项目三件套（脚本/网页/工作流）并验证通过。
- 2026-08-02：项目部署完成——git 提交推送 → GitHub Pages 上线（HTTP 200）→ Actions 手动触发测试成功，自动化闭环全部验证通过。
