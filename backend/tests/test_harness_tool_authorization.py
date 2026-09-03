from app.harness.context import HarnessContext
from app.harness.tool_authorization import ToolAuthorization
from app.harness.tool_registry import ToolDefinition, ToolRegistry


def create_context(*allowed_tools: str) -> HarnessContext:
    return HarnessContext(
        task_id="task-123",
        workspace="/workspace/demo",
        instruction="Run the requested task",
        allowed_tools=allowed_tools,
    )


def test_authorizes_registered_and_allowed_tool() -> None:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="filesystem",
            description="Read and write workspace files",
        )
    )

    authorization = ToolAuthorization(registry)
    context = create_context("filesystem")

    assert authorization.is_authorized("filesystem", context) is True


def test_denies_registered_but_not_allowed_tool() -> None:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="terminal",
            description="Execute approved terminal commands",
        )
    )

    authorization = ToolAuthorization(registry)
    context = create_context()

    assert authorization.is_authorized("terminal", context) is False


def test_denies_unknown_tool() -> None:
    registry = ToolRegistry()

    authorization = ToolAuthorization(registry)
    context = create_context("unknown")

    assert authorization.is_authorized("unknown", context) is False
