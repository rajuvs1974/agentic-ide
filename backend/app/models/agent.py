from dataclasses import dataclass
from enum import StrEnum


class AgentTaskStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentTask:
    task_id: str
    instruction: str
    workspace: str


@dataclass(frozen=True)
class AgentExecutionResult:
    task_id: str
    status: AgentTaskStatus
    message: str
