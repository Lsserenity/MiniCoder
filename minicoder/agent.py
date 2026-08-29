import json
from pathlib import Path

from minicoder.llm.openai_client import LLMClient
from minicoder.tools.definitions import TOOLS
from minicoder.tools.manager import ToolManager


SYSTEM_PROMPT = """
You are MiniCoder, a coding agent working inside a local project workspace.

Use the available tools when you need information about the project.
Do not guess file contents or project structure.
Inspect the project before making conclusions.
"""


class Agent:
    def __init__(
        self,
        workspace: Path,
        max_steps: int = 20,
    ) -> None:
        
        self.workspace = workspace.resolve()
        self.llm = LLMClient()
        self.tool_manager = ToolManager(
            workspace=self.workspace
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
            # llm的回答
            message = self.llm.chat(
                messages=self.messages,
                tools=TOOLS,
            )

            self.messages.append(message)

            # 如果没有工具调用，说明当前对话可以结束，返回模型回答的内容
            if not message.tool_calls:
                return message.content or ""
            # 否则依次执行工具调用
            for tool_call in message.tool_calls:
                result = self.tool_manager.execute(
                    tool_call
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