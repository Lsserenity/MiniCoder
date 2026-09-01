import json
from pathlib import Path

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


def reject_confirmation(
    tool_name: str,
    arguments: dict,
    reason: str,
) -> bool:
    print(
        "confirmation requested:",
        tool_name,
        arguments,
        reason,
    )

    return False


def main():
    manager = ToolManager(
        workspace=Path(".").resolve(),
    )

    tool_call = MockToolCall(
        name="run_command",
        arguments=json.dumps(
            {
                "command":
                    "pip install flask"
            }
        ),
    )

    result = manager.execute(
        tool_call
    )

    print(result)


if __name__ == "__main__":
    main()