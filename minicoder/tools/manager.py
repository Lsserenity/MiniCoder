import json
from pathlib import Path

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
    Manage and execute local tools requested by the LLM.
    """

    # 需要传入workspace作为参数
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

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