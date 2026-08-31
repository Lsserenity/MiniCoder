import json
from pathlib import Path

from minicoder.policy.engine import PolicyAction, PolicyEngine
from minicoder.tools.filesystem import list_files, read_file, write_file, edit_file
from minicoder.tools.search import search_text
from minicoder.tools.shell import run_command

# 映射的是函数本身
TOOL_REGISTRY = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "search_text": search_text,
    "run_command": run_command,
}


class ToolManager:
    """
    规划并执行工具调用的管理器。它接收LLM的tool_call对象，执行对应的工具函数，并返回结果。
    """

    # 需要传入workspace作为参数
    def __init__(
        self,
        workspace: Path,
    ) -> None:
        self.workspace = workspace.resolve()
        self.policy = PolicyEngine()

    # 接收llm的tool_call对象，返回执行结果，字典
    def execute(self, tool_call) -> dict:
        """
        Execute one tool call returned by the LLM.
        """

        tool_name = tool_call.function.name

        if tool_name not in TOOL_REGISTRY:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
            }

        try:
            arguments = json.loads(
                tool_call.function.arguments
            )
        except json.JSONDecodeError as exc:
            return {
                "success": False,
                "error": (
                    f"Invalid JSON arguments: {exc}"
                ),
            }

        tool = TOOL_REGISTRY[tool_name]

        # 检查工具调用是否合法
        decision = (
            self.policy.check_tool_call(
                tool_name=tool_name,
                arguments=arguments,
            )
        )

        if decision.action == PolicyAction.DENY:
            return {
                "success": False,
                "error": (
                    "Tool call denied by policy: "
                    f"{decision.reason}"
                ),
                "policy_action": (
                    decision.action.value
                ),
            }

        # 目前保留REQUIRE_CONFIRMATION，等待后续交互逻辑完善
        if (
            decision.action
            == PolicyAction.REQUIRE_CONFIRMATION
        ):
            return {
                "success": False,
                "error": (
                    "Tool call requires user "
                    "confirmation before execution: "
                    f"{decision.reason}"
                ),
                "policy_action": (
                    decision.action.value
                ),
            }
        
        try:
            result = tool(
                workspace=self.workspace,
                **arguments,
            )
        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
            }

        return result