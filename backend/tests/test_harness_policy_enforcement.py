from app.harness.context import HarnessContext
from app.harness.policy import HarnessPolicy
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.tool_authorization import ToolAuthorization
from app.harness.tool_registry import ToolDefinition, ToolRegistry


def create_enforcement() -> PolicyEnforcement:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="filesystem",
            description="Read and write workspace files",
            handler=lambda arguments: arguments,
        )
    )

    authorization = ToolAuthorization(registry)
    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
    )

    return PolicyEnforcement(authorization, policy)


def create_context(
    workspace: str = "/workspace/demo",
    *allowed_tools: str,
) -> HarnessContext:
    return HarnessContext(
        task_id="task-123",
        workspace=workspace,
        instruction="Perform the requested task",
        allowed_tools=allowed_tools,
    )


def test_allows_registered_tool_in_allowed_workspace() -> None:
    enforcement = create_enforcement()
    context = create_context("/workspace/demo", "filesystem")

    assert enforcement.can_use_tool("filesystem", context) is True


def test_denies_tool_outside_policy_workspace() -> None:
    enforcement = create_enforcement()
    context = create_context("/workspace/other", "filesystem")

    assert enforcement.can_use_tool("filesystem", context) is False


def test_denies_tool_not_allowed_by_context() -> None:
    enforcement = create_enforcement()
    context = create_context("/workspace/demo")

    assert enforcement.can_use_tool("filesystem", context) is False
