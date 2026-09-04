from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ToolExecutionStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    status: ToolExecutionStatus
    output: Any = None
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.status == ToolExecutionStatus.SUCCESS