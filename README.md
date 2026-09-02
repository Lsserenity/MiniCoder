## MiniCoder

https://github.com/Lsserenity/MiniCoder.git

### 项目情况

MiniCoder 是一个基于 Python 3.11 开发的轻量级本地 Coding Agent，当前使用智谱 GLM-4.7-Flash 作为语言模型，以 CLI 形式提供交互，并支持本地代码理解、修改、命令执行、任务规划与安全控制。

### 运行说明

运行环境：Python 3.11

安装依赖：
`pip install -r requirements.txt`

配置：
复制 `.env.example` 为 `.env` 并填写 `MODEL_API_KEY`。当前默认通过智谱开放平台的 OpenAI 兼容接口调用 GLM-4.7-Flash，也可通过 `MODEL_BASE_URL` 和 `MODEL_NAME` 配置其他兼容模型服务。

运行：
`python -m minicoder <workspace>`

示例：
`python -m minicoder demo_todo`

### 主要功能

1. 多轮 Agent Loop：维护当前 CLI 会话的消息历史，根据模型 Tool Call 自动执行工具并将结果反馈给模型继续推理。
2. 本地工具：支持文件列表与读取、精确编辑、文件写入、文本搜索和 Shell 命令执行。
3. 显式任务规划：通过 `update_plan` 维护 pending、in_progress、completed 状态，并支持 `/plan` 查看。
4. 安全控制：限制文件访问范围；命令支持超时和输出截断；PolicyEngine 将操作划分为允许、拒绝和需用户确认三类。
5. 交互式 CLI：支持 `/help`、`/plan`、`/diff`、`/exit`，其中 `/diff` 可查看 Git workspace 的未提交修改。
6. 回归测试：运行 `python -m pytest -v` 可验证主要 Runtime 功能。

### 补充说明

当前消息历史和计划状态保存在单次 CLI 进程中，暂未实现跨进程 Session Persistence；当前安全机制属于应用层权限控制，未实现操作系统级 Sandbox，后续可进一步扩展。