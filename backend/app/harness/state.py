from dataclasses import dataclass
from enum import StrEnum


class HarnessExecutionStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    TOOL_CALL = "tool_call"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class HarnessState:
    task_id: str
    status: HarnessExecutionStatus = HarnessExecutionStatus.CREATED

    def transition(
        self,
        status: HarnessExecutionStatus,
    ) -> "HarnessState":
        allowed_transitions = {
            HarnessExecutionStatus.CREATED: {
                HarnessExecutionStatus.RUNNING,
                HarnessExecutionStatus.FAILED,
            },
            HarnessExecutionStatus.RUNNING: {
                HarnessExecutionStatus.TOOL_CALL,
                HarnessExecutionStatus.VERIFYING,
                HarnessExecutionStatus.COMPLETED,
                HarnessExecutionStatus.FAILED,
            },
            HarnessExecutionStatus.TOOL_CALL: {
                HarnessExecutionStatus.RUNNING,
                HarnessExecutionStatus.VERIFYING,
                HarnessExecutionStatus.FAILED,
            },
            HarnessExecutionStatus.VERIFYING: {
                HarnessExecutionStatus.COMPLETED,
                HarnessExecutionStatus.FAILED,
            },
            HarnessExecutionStatus.COMPLETED: set(),
            HarnessExecutionStatus.FAILED: set(),
        }

        if status not in allowed_transitions[self.status]:
            raise ValueError(
                f"Invalid state transition: "
                f"{self.status.value} -> {status.value}"
            )

        return HarnessState(
            task_id=self.task_id,
            status=status,
        )
