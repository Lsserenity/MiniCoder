from minicoder.planning.plan import (
    PlanState,
    PlanStatus,
    PlanStep,
)


def test_plan_state_stores_steps() -> None:
    state = PlanState()

    state.set_steps(
        [
            PlanStep(
                description="Inspect",
                status=(
                    PlanStatus.IN_PROGRESS
                ),
            ),
            PlanStep(
                description="Test",
                status=(
                    PlanStatus.PENDING
                ),
            ),
        ]
    )

    result = state.to_dict()

    assert len(result["steps"]) == 2
    assert (
        result["steps"][0]["status"]
        == "in_progress"
    )