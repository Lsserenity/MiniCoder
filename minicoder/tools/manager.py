import json
from pathlib import Path

from minicoder.policy.engine import (
    PolicyAction,
    PolicyEngine,
)
from minicoder.planning.plan import (
    PlanState,
    PlanStatus,
    PlanStep,
)
from minicoder.tools.filesystem import (
    list_files,
    read_file,
    write_file,
    edit_file,
)
from minicoder.tools.search import search_text
from minicoder.tools.shell import run_command


# 普通工具注册表
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
    MiniCoder 的统一工具执行入口。

    它负责：
    1. 接收 LLM 返回的 tool_call
    2. 解析 JSON 参数
    3. 分发 Runtime Tool
    4. 查找普通工具
    5. 执行 Policy 检查
    6. 注入 workspace 并执行工具
    7. 捕获工具执行异常
    """

    def __init__(
        self,
        workspace: Path,
        plan_state: PlanState | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.policy = PolicyEngine()

        if plan_state is None:
            self.plan_state = PlanState()
        else:
            self.plan_state = plan_state

    def execute(
        self,
        tool_call,
    ) -> dict:
        """
        执行一个由 LLM 返回的 tool call。
        """

        tool_name = tool_call.function.name

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

        # Runtime Tool 特殊处理
        # update_plan 不操作 workspace，
        # 它操作的是 MiniCoder 自己的 PlanState，
        # 所以不进入普通 TOOL_REGISTRY。
        if tool_name == "update_plan":
            return self._update_plan(
                arguments
            )

        # 查找普通工具
        if tool_name not in TOOL_REGISTRY:
            return {
                "success": False,
                "error": (
                    f"Unknown tool: {tool_name}"
                ),
            }

        tool = TOOL_REGISTRY[
            tool_name
        ]

        # PolicyEngine 检查
        decision = (
            self.policy.check_tool_call(
                tool_name=tool_name,
                arguments=arguments,
            )
        )

        if (
            decision.action
            == PolicyAction.DENY
        ):
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

        # 当前版本还没有真正的 CLI confirmation。
        # 所以遇到 REQUIRE_CONFIRMATION 时先不执行，
        # 只把结果返回给 Agent。
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

        # 真正执行普通工具
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

    def _update_plan(
        self,
        arguments: dict,
    ) -> dict:
        """
        更新 MiniCoder 当前任务的显式计划状态。
        模型输入的形式：
        {
            "steps": [
                {
                    "description": "...",
                    "status": "pending"
                }
            ]
        }
        """

        raw_steps = arguments.get(
            "steps"
        )

        if not isinstance(
            raw_steps,
            list,
        ):
            return {
                "success": False,
                "error": (
                    "steps must be a list."
                ),
            }

        # 先创建一份新的 plan，
        # 全部验证成功以后再替换旧 plan。
        new_steps = []

        for raw_step in raw_steps:
            if not isinstance(
                raw_step,
                dict,
            ):
                return {
                    "success": False,
                    "error": (
                        "Each plan step must "
                        "be an object."
                    ),
                }

            description = raw_step.get(
                "description"
            )

            status_value = raw_step.get(
                "status"
            )

            # description 必须是非空字符串
            if (
                not isinstance(
                    description,
                    str,
                )
                or not description.strip()
            ):
                return {
                    "success": False,
                    "error": (
                        "Each plan step must "
                        "have a non-empty "
                        "description."
                    ),
                }

            # 把模型传来的字符串转换成 Runtime 内部的 PlanStatus Enum
            try:
                status = PlanStatus(
                    status_value
                )
            except ValueError:
                return {
                    "success": False,
                    "error": (
                        "Invalid plan status: "
                        f"{status_value}"
                    ),
                }

            # 参数合法以后才真正创建 PlanStep
            new_steps.append(
                PlanStep(
                    description=(
                        description.strip()
                    ),
                    status=status,
                )
            )

        self.plan_state.set_steps(
            new_steps
        )

        return {
            "success": True,
            "plan": (
                self.plan_state.to_dict()
            ),
        }