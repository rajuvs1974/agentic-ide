from collections.abc import Callable
from typing import Any, cast
from unittest.mock import Mock

from app.harness.context import HarnessContext
from app.harness.policy import HarnessPolicy
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.tool_authorization import ToolAuthorization
from app.harness.tool_execution import (
    ToolExecutionStatus,
    ToolRequest,
)
from app.harness.tool_executor import ToolExecutor
from app.harness.tool_registry import ToolDefinition, ToolRegistry


def create_executor(
    handler: Callable[[dict[str, Any]], Any] | None = None,
) -> tuple[ToolExecutor, Mock]:
    registry = ToolRegistry()

    tool_handler = (
        Mock(return_value="hello")
        if handler is None
        else handler
    )

    registry.register(
        ToolDefinition(
            name="echo",
            description="Returns a message",
            handler=cast(
                Callable[[dict[str, Any]], Any],
                tool_handler,
            ),
        )
    )

    authorization = ToolAuthorization(registry)
    policy = HarnessPolicy(
        workspace_scope="/workspace/project",
    )
    policy_enforcement = PolicyEnforcement(
        authorization,
        policy,
    )

    return (
        ToolExecutor(
            registry,
            policy_enforcement,
        ),
        cast(Mock, tool_handler),
    )





def create_context(
    *,
    workspace: str = "/workspace/project",
    allowed_tools: tuple[str, ...] = ("echo",),
) -> HarnessContext:
    return HarnessContext(
        task_id="task-001",
        workspace=workspace,
        instruction="Test tool execution",
        allowed_tools=allowed_tools,
    )


def test_tool_executor_executes_authorized_tool() -> None:
    executor, handler = create_executor()
    context = create_context()

    result = executor.execute(
        ToolRequest(
            tool_name="echo",
            arguments={"message": "hello"},
        ),
        context,
    )

    assert result.status == ToolExecutionStatus.SUCCESS
    assert result.succeeded is True
    assert result.output == "hello"
    assert result.error is None
    handler.assert_called_once_with({"message": "hello"})


def test_tool_executor_denies_unauthorized_tool() -> None:
    executor, handler = create_executor()
    context = create_context(allowed_tools=())

    result = executor.execute(
        ToolRequest(
            tool_name="echo",
            arguments={"message": "hello"},
        ),
        context,
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool not authorized: echo"
    handler.assert_not_called()


def test_tool_executor_denies_tool_outside_policy_workspace() -> None:
    executor, handler = create_executor()
    context = create_context(
        workspace="/workspace/other",
    )

    result = executor.execute(
        ToolRequest(
            tool_name="echo",
            arguments={"message": "hello"},
        ),
        context,
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool not authorized: echo"
    handler.assert_not_called()


def test_tool_executor_returns_failure_for_unknown_tool() -> None:
    executor, _ = create_executor()
    context = create_context()

    result = executor.execute(
        ToolRequest(
            tool_name="missing",
            arguments={},
        ),
        context,
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool not found: missing"


def test_tool_executor_returns_failure_when_tool_raises() -> None:
    failing_handler = Mock(
        side_effect=RuntimeError("Tool execution failed"),
    )

    executor, handler = create_executor(
        handler=failing_handler,
    )
    context = create_context()

    result = executor.execute(
        ToolRequest(
            tool_name="echo",
            arguments={},
        ),
        context,
    )

    assert result.status == ToolExecutionStatus.FAILED
    assert result.succeeded is False
    assert result.error == "Tool execution failed"
    handler.assert_called_once_with({})
