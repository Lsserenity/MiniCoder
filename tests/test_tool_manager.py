import json
from pathlib import Path

from minicoder.tools.manager import ToolManager


class MockFunction:
    def __init__(
        self,
        name: str,
        arguments: str,
    ) -> None:
        self.name = name
        self.arguments = arguments


class MockToolCall:
    def __init__(
        self,
        name: str,
        arguments: str,
    ) -> None:
        self.function = MockFunction(
            name=name,
            arguments=arguments,
        )


def reject_confirmation(
    tool_name: str,
    arguments: dict,
    reason: str,
) -> bool:
    return False


def test_confirmation_can_be_rejected(
    tmp_path: Path,
) -> None:
    manager = ToolManager(
        workspace=tmp_path,
        confirmation_handler=(
            reject_confirmation
        ),
    )

    tool_call = MockToolCall(
        name="run_command",
        arguments=json.dumps(
            {
                "command":
                    "python -m pip install flask"
            }
        ),
    )

    result = manager.execute(
        tool_call
    )

    assert result["success"] is False
    assert (
        result["policy_action"]
        == "rejected"
    )