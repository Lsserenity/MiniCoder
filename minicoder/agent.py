import json
from collections.abc import Callable
from pathlib import Path

from minicoder.llm.openai_client import LLMClient
from minicoder.planning.plan import PlanState
from minicoder.tools.definitions import TOOLS
from minicoder.tools.manager import ToolManager
from minicoder.ui.terminal import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RED,
    format_tool_result,
    pretty_json,
    style,
)


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
8. For multi-step coding tasks, create and maintain a concise explicit plan
   using update_plan. Ground the plan in the actual task and observed project
   structure. Keep exactly one step in_progress while work is active, mark
   finished steps completed, and keep remaining steps pending. Avoid speculative
   steps for files, frameworks, or components that have not been observed.
9. Avoid repeating the same tool call with the same arguments when the previous
   result is still valid.
10. Do not overstate conclusions. Only make claims that are directly supported
    by inspected code, command output, or test results.
11. Once the requested verification has succeeded, do not perform additional
    speculative investigation unless there is concrete evidence of a problem.
12. When analyzing unfamiliar framework behavior, do not infer correctness
    solely from implementation details or private attributes. Prefer observed
    behavior and documented project conventions.
"""


class Agent:
    def __init__(
        self,
        workspace: Path,
        max_steps: int = 20,
        confirmation_handler: Callable[
            [str, dict, str],
            bool,
        ]
        | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.llm = LLMClient()
        self.plan_state = PlanState()

        self.tool_manager = ToolManager(
            workspace=self.workspace,
            plan_state=self.plan_state,
            confirmation_handler=confirmation_handler,
        )

        self.max_steps = max_steps

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def run(
        self,
        user_input: str,
    ) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        for step in range(
            self.max_steps
        ):
            print(
                style(
                    f"[agent] step {step + 1}",
                    CYAN,
                    DIM,
                )
            )

            try:
                message = self.llm.chat(
                    messages=self.messages,
                    tools=TOOLS,
                )

            except Exception as exc:
                print(
                    style(
                        "[error] LLM request failed",
                        RED,
                        BOLD,
                    )
                )

                return (
                    "Agent stopped because the "
                    "LLM request failed. "
                    "Changes already made to the "
                    "workspace were not automatically "
                    "rolled back. "
                    f"Error: {exc}"
                )

            self.messages.append(
                message
            )

            if not message.tool_calls:
                print(
                    style(
                        "[agent] final response",
                        CYAN,
                        DIM,
                    )
                )

                return message.content or ""

            for tool_call in message.tool_calls:
                tool_name = (
                    tool_call.function.name
                )

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                except json.JSONDecodeError:
                    arguments = {
                        "raw":
                            tool_call.function.arguments
                    }

                print()

                print(
                    style(
                        f"[tool] {tool_name}",
                        GREEN,
                        BOLD,
                    )
                )

                argument_text = pretty_json(
                    arguments
                )

                for line in (
                    argument_text.splitlines()
                ):
                    print(
                        f"       "
                        f"{style(line, DIM)}"
                    )

                result = (
                    self.tool_manager.execute(
                        tool_call
                    )
                )

                success = result.get(
                    "success",
                    False,
                )

                result_status = (
                    "success"
                    if success
                    else "failed"
                )

                result_color = (
                    GREEN
                    if success
                    else RED
                )

                result_text = (
                    format_tool_result(
                        tool_name,
                        result,
                    )
                )

                print()

                print(
                    f"{style('[result]', result_color, BOLD)} "
                    f"{style(result_status, result_color)}"
                )

                for line in (
                    result_text.splitlines()
                ):
                    print(
                        f"         {line}"
                    )

                tool_message = {
                    "role": "tool",
                    "tool_call_id":
                        tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }

                self.messages.append(
                    tool_message
                )

        return (
            "Agent stopped because the "
            "maximum number of steps "
            "was reached."
        )