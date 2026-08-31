import json
from pathlib import Path

from minicoder.llm.openai_client import LLMClient
from minicoder.tools.definitions import TOOLS
from minicoder.tools.manager import ToolManager
from minicoder.planning.plan import PlanState


SYSTEM_PROMPT = """
You are MiniCoder, a coding agent working inside a local project workspace.

Use the available tools to inspect, modify, and verify the project.

Follow these rules:
1. Do not guess file contents or project structure. Inspect relevant files first.
2. Prefer precise edits over overwriting entire existing files when possible.
3. If a tool call fails, inspect the error and try a reasonable recovery strategy.
4. After modifying code, run relevant tests or commands whenever possible.
5. If verification fails, inspect the failure, fix the problem, and verify again.
6. Do not claim a task is complete unless the requested changes are implemented
   and relevant verification has succeeded when verification is available.
7. Do not install packages or modify the system environment unless the user
   explicitly asks you to do so.
8. For multi-step coding tasks, create and maintain an explicit plan using
   update_plan. Keep exactly one step in_progress when work is active, mark
   finished steps completed, and keep remaining steps pending.
9. Avoid repeating the same tool call with the same arguments when the previous
   result is still valid.
   
Do not overstate verification results.
Only claim what the observed tests and tool results support.
"""


class Agent:
    def __init__(
        self,
        workspace: Path,
        max_steps: int = 20,
    ) -> None:
        
        self.workspace = workspace.resolve()
        self.llm = LLMClient()
        self.plan_state = PlanState()
        self.tool_manager = ToolManager(
            workspace=self.workspace,
            plan_state=self.plan_state,
        )
        self.max_steps = max_steps
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def run(self, user_input: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        for step in range(self.max_steps):
            # 调试信息
            print(
                f"[Agent] step {step + 1}",
            )
            # llm的回答
            try:
                message = self.llm.chat(
                    messages=self.messages,
                    tools=TOOLS,
                )
            except Exception as exc:
                return (
                    "Agent stopped because the LLM request failed. "
                    "Changes already made to the workspace were not "
                    "automatically rolled back. "
                    f"Error: {exc}"
                )

            self.messages.append(message)

            # 如果没有工具调用，说明当前对话可以结束，返回模型回答的内容
            if not message.tool_calls:
                # 调试
                print(
                    "[Agent] No tool call. "
                    "Returning final answer."
                )
                return message.content or ""
            # 否则依次执行工具调用
            for tool_call in message.tool_calls:
                # 调试信息
                print(
                    f"[Agent] Calling tool: "
                    f"{tool_call.function.name}"
                )

                print(
                    f"[Agent] Arguments: "
                    f"{tool_call.function.arguments}"
                )

                result = self.tool_manager.execute(
                    tool_call
                )

                # 调试
                print(
                    f"[Agent] Tool result: {result}"
                )

                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }

                self.messages.append(tool_message)

        return (
            "Agent stopped because the maximum "
            "number of steps was reached."
        )