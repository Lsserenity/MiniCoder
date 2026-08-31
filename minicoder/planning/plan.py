from dataclasses import dataclass
from enum import Enum

# 计划执行状态
class PlanStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class PlanStep:
    description: str
    status: PlanStatus

class PlanState:
    def __init__(self) -> None:
        self.steps: list[PlanStep] = []

    def set_steps(
        self,
        steps: list[PlanStep],
    ) -> None:
        self.steps = steps

    def to_dict(self) -> dict:
        return {
            "steps": [
                {
                    "description": step.description,
                    "status": step.status.value,
                }
                for step in self.steps
            ]
        }
