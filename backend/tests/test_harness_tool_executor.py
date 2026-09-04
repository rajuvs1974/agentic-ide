from app.harness.tool_execution import (
    ToolExecutionStatus,
    ToolRequest,
)
from app.harness.tool_executor import ToolExecutor
from app.harness.tool_registry import ToolDefinition, ToolRegistry


def test_tool_executor_executes_registered_tool() -> None:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="echo",
            description="Returns the supplied message",
            handler=lambda arguments: arguments["message"],
        )
    )

    executor = ToolExecutor(registry)

    result = executor.execute(
        ToolRequest(
            tool_name="echo",
            arguments={"message": "hello"},
        )
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.succeeded is True
    assert result.output == "hello"
    assert result.error is None


def test_tool_executor_returns_failure_for_unknown_tool() -> None:
    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = executor.execute(
        ToolRequest(
            tool_name="missing",
            arguments={},
        )
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool not found: missing"


def test_tool_executor_returns_failure_when_tool_raises() -> None:
    registry = ToolRegistry()

    def failing_tool(arguments: dict[str, object]) -> object:
        raise RuntimeError("Tool execution failed")

    registry.register(
        ToolDefinition(
            name="failing",
            description="Always fails",
            handler=failing_tool,
        )
    )

    executor = ToolExecutor(registry)

    result = executor.execute(
        ToolRequest(
            tool_name="failing",
            arguments={},
        )
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool execution failed"