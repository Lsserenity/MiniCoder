import json
from pathlib import Path

from minicoder.planning.plan import PlanState
from minicoder.tools.manager import ToolManager


class MockFunction:
    def __init__(
        self,
        name: str,
        arguments: str,
    ):
        self.name = name
        self.arguments = arguments


class MockToolCall:
    def __init__(
        self,
        name: str,
        arguments: str,
    ):
        self.function = MockFunction(
            name,
            arguments,
        )


def main():
    plan_state = PlanState()

    manager = ToolManager(
        workspace=Path(
            "demo_todo"
        ).resolve(),
        plan_state=plan_state,
    )

    arguments = json.dumps(
        {
            "steps": [
                {
                    "description":
                        "Inspect project",
                    "status":
                        "completed",
                },
                {
                    "description":
                        "Fix failing test",
                    "status":
                        "in_progress",
                },
                {
                    "description":
                        "Run tests",
                    "status":
                        "pending",
                },
            ]
        }
    )

    tool_call = MockToolCall(
        name="update_plan",
        arguments=arguments,
    )

    result = manager.execute(
        tool_call
    )

    print("tool result:")
    print(result)

    print("runtime plan:")
    print(
        plan_state.to_dict()
    )


if __name__ == "__main__":
    main()