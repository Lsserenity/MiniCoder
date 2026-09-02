## MiniCoder

https://github.com/Lsserenity/MiniCoder

MiniCoder 是一个基于 Python 3.11 的轻量级本地 Coding Agent。它通过 CLI 与用户交互，调用 OpenAI 兼容接口中的 GLM-4.7-Flash，并使用本地工具完成代码理解、文件修改、命令执行、任务规划和基础安全控制。

### 运行

安装依赖：

```bash
pip install -r requirements.txt
```

复制 `.env.example` 为 `.env`，填写 `MODEL_API_KEY`，并按需配置 `MODEL_BASE_URL`、`MODEL_NAME`。

启动：

```bash
python -m minicoder <workspace>
```

示例：

```bash
python -m minicoder demo_todo
```

### 功能

1. 多轮 Agent Loop：维护当前 CLI 会话上下文，处理模型返回的 tool call，并把工具结果继续反馈给模型。
2. 本地工具：支持文件列表、读取、写入、精确替换、文本搜索和 Shell 命令执行。
3. 任务规划：通过 `update_plan` 维护 `pending`、`in_progress`、`completed` 状态，并可用 `/plan` 查看。
4. CLI 命令：支持 `/help`、`/plan`、`/diff`、`/exit`。
5. 回归测试：运行 `python -m pytest -v` 验证主要 Runtime 行为。

### 安全说明

文件工具会限制路径在 workspace 内，并阻止读取、写入或编辑 `.env` 等敏感文件；搜索工具也会跳过敏感文件。Shell 命令从 workspace 启动，支持超时和输出截断，并由 PolicyEngine 对明显危险命令进行拒绝，对安装依赖、联网请求、读取敏感配置和输出重定向等操作要求用户确认。

当前安全机制属于应用层控制，不是操作系统级 Sandbox。Shell 命令仍继承当前用户权限，因此不能视为完全隔离环境。
