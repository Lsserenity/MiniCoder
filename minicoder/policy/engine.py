from dataclasses import dataclass
from enum import Enum

DENIED_COMMAND_PATTERNS = (
    "rm -rf",
    "rm -fr",
    "rm -r ",
    "del /s",
    "del /f",
    "del /q",
    "erase /s",
    "format ",
    "rd /s",
    "rmdir /s",
    "remove-item -recurse",
    "remove-item -r",
    "remove-item -force",
    "shutdown",
    "reboot",
    "git reset --hard",
    "git clean -fd",
    "git clean -xdf",
)

CONFIRMATION_COMMAND_PATTERNS = (
    "pip install",
    "pip uninstall",
    "python -m pip install",
    "python -m pip uninstall",
    "conda install",
    "conda remove",
    "npm install",
    "npm uninstall",
    "npm update",
    "apt install",
    "apt-get install",
    "curl ",
    "wget ",
    "invoke-webrequest",
    "invoke-restmethod",
    "type .env",
    "cat .env",
    "get-content .env",
    ">",
)

class PolicyAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_CONFIRMATION = "require_confirmation"

@dataclass
class PolicyDecision:
    action: PolicyAction
    reason: str

class PolicyEngine:
    # 检查工具调用是否合法，返回Policy Decision对象
    def check_tool_call(
        self,
        tool_name: str,
        arguments: dict,
    ) -> PolicyDecision:
        if tool_name == "run_command":
            return self._check_command(
                arguments
            )

        return PolicyDecision(
            action=PolicyAction.ALLOW,
            reason=(
                f"No restrictive policy "
                f"for tool: {tool_name}"
            ),
        )

    # 私有函数，检查command是否合法，返回Policy Decision对象 
    def _check_command(
        self,
        arguments: dict,
    ) -> PolicyDecision:
        command = arguments.get(
            "command",
            "",
        )

        if not isinstance(command, str):
            return PolicyDecision(
                action=PolicyAction.DENY,
                reason=(
                    "Command must be a string."
                ),
            )

        normalized_command = (
            command.strip().lower()
        )

        if not normalized_command:
            return PolicyDecision(
                action=PolicyAction.DENY,
                reason=(
                    "Empty commands are not allowed."
                ),
            )

        for pattern in DENIED_COMMAND_PATTERNS:
            if pattern in normalized_command:
                return PolicyDecision(
                    action=PolicyAction.DENY,
                    reason=(
                        "Command matches a blocked "
                        f"pattern: {pattern}"
                    ),
                )

        for pattern in (
            CONFIRMATION_COMMAND_PATTERNS
        ):
            if pattern in normalized_command:
                return PolicyDecision(
                    action=(
                        PolicyAction
                        .REQUIRE_CONFIRMATION
                    ),
                    reason=(
                        "Command modifies the "
                        "development environment "
                        "and requires user approval."
                    ),
                )

        return PolicyDecision(
            action=PolicyAction.ALLOW,
            reason=(
                "Command passed the current "
                "runtime policy."
            ),
        )
