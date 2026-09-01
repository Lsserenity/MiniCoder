from minicoder.policy.engine import (
    PolicyAction,
    PolicyEngine,
)


def test_policy_denies_shutdown() -> None:
    engine = PolicyEngine()

    decision = engine.check_tool_call(
        tool_name="run_command",
        arguments={
            "command": "shutdown /s"
        },
    )

    assert (
        decision.action
        == PolicyAction.DENY
    )


def test_policy_requires_confirmation_for_pip() -> None:
    engine = PolicyEngine()

    decision = engine.check_tool_call(
        tool_name="run_command",
        arguments={
            "command":
                "python -m pip install flask"
        },
    )

    assert (
        decision.action
        == PolicyAction.REQUIRE_CONFIRMATION
    )


def test_policy_allows_normal_command() -> None:
    engine = PolicyEngine()

    decision = engine.check_tool_call(
        tool_name="run_command",
        arguments={
            "command":
                "python -c \"print('ok')\""
        },
    )

    assert (
        decision.action
        == PolicyAction.ALLOW
    )