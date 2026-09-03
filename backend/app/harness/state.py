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
