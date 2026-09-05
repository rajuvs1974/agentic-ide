
from app.harness.context import HarnessContext
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.tool_execution import (
    ToolExecutionStatus,
    ToolRequest,
    ToolResult,
)
from app.harness.tool_registry import ToolRegistry


class ToolExecutor:
    def __init__(
        self,
        registry: ToolRegistry,
        policy_enforcement: PolicyEnforcement,
    ) -> None:
        self._registry = registry
        self._policy_enforcement = policy_enforcement


    def execute(
    self,
    request: ToolRequest,
    context: HarnessContext,
        ) -> ToolResult:
        tool = self._registry.get(request.tool_name)

        if tool is None:
            return ToolResult(
            tool_name=request.tool_name,
            status=ToolExecutionStatus.FAILED,
            error=f"Tool not found: {request.tool_name}",
        )

        if not self._policy_enforcement.can_use_tool(
        request.tool_name,
        context,
        ):
            return ToolResult(
            tool_name=request.tool_name,
            status=ToolExecutionStatus.FAILED,
            error=f"Tool not authorized: {request.tool_name}",
        )

        try:
            output = tool.handler(request.arguments)
            return ToolResult(
            tool_name=request.tool_name,
            status=ToolExecutionStatus.SUCCESS,
            output=output,
        )
        except Exception as exc:  # noqa: BLE001
            return ToolResult(
            tool_name=request.tool_name,
            status=ToolExecutionStatus.FAILED,
            error=str(exc),
        )

