from app.harness.tool_execution import (
    ToolExecutionStatus,
    ToolRequest,
    ToolResult,
)
from app.harness.tool_registry import ToolRegistry


class ToolExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def execute(self, request: ToolRequest) -> ToolResult:
        tool = self._registry.get(request.tool_name)

        if tool is None:
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolExecutionStatus.FAILED,
                error=f"Tool not found: {request.tool_name}",
            )

        try:
            output = tool.handler(request.arguments)

            return ToolResult(
                tool_name=request.tool_name,
                status=ToolExecutionStatus.SUCCESS,
                output=output,
            )
        except Exception as exc: # noqa: BLE001
            return ToolResult(
                tool_name=request.tool_name,
                status=ToolExecutionStatus.FAILED,
                error=str(exc),
            )