import pytest

from app.harness.context import HarnessContext
from app.harness.instructions import HarnessInstructions
from app.harness.orchestrator import HarnessExecution, HarnessOrchestrator
from app.harness.policy import HarnessPolicy
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.state import HarnessExecutionStatus
from app.harness.tool_authorization import ToolAuthorization
from app.harness.tool_registry import ToolDefinition, ToolRegistry
from app.harness.verification import VerificationResult, VerificationStatus
from app.harness.verification_engine import VerificationEngine


def create_orchestrator() -> HarnessOrchestrator:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="filesystem",
            description="Read and write workspace files",
        )
    )

    authorization = ToolAuthorization(registry)
    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
    )
    enforcement = PolicyEnforcement(authorization, policy)

    return HarnessOrchestrator(enforcement)


def create_execution() -> tuple[HarnessOrchestrator, HarnessExecution]:
    orchestrator = create_orchestrator()

    context = HarnessContext(
        task_id="task-123",
        workspace="/workspace/demo",
        instruction="Implement the health endpoint",
        allowed_tools=("filesystem",),
    )

    instructions = HarnessInstructions(
        system="You are a software engineering agent.",
        task=context.instruction,
    )

    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
        require_verification=True,
    )

    execution = orchestrator.create_execution(
        context=context,
        instructions=instructions,
        policy=policy,
    )

    return orchestrator, execution


def test_orchestrator_creates_harness_execution() -> None:
    orchestrator, execution = create_execution()

    assert execution.context.task_id == "task-123"
    assert execution.context.workspace == "/workspace/demo"
    assert execution.instructions.task == "Implement the health endpoint"
    assert execution.policy.require_verification is True
    assert execution.state.task_id == "task-123"
    assert execution.state.status == HarnessExecutionStatus.CREATED
    assert orchestrator.can_use_tool(execution, "filesystem") is True


def test_orchestrator_denies_tool_not_allowed_by_context() -> None:
    orchestrator, execution = create_execution()

    restricted_context = HarnessContext(
        task_id=execution.context.task_id,
        workspace=execution.context.workspace,
        instruction=execution.context.instruction,
    )

    restricted_execution = orchestrator.create_execution(
        context=restricted_context,
        instructions=execution.instructions,
        policy=execution.policy,
    )

    assert orchestrator.can_use_tool(
        restricted_execution,
        "filesystem",
    ) is False


def test_orchestrator_denies_unknown_tool() -> None:
    orchestrator, execution = create_execution()

    assert orchestrator.can_use_tool(
        execution,
        "terminal",
    ) is False


def test_orchestrator_manages_execution_lifecycle() -> None:
    orchestrator, execution = create_execution()

    execution = orchestrator.start(execution)
    assert execution.state.status == HarnessExecutionStatus.RUNNING

    execution = orchestrator.begin_tool_call(execution)
    assert execution.state.status == HarnessExecutionStatus.TOOL_CALL

    execution = orchestrator.begin_verification(execution)
    assert execution.state.status == HarnessExecutionStatus.VERIFYING

    verification = VerificationEngine().evaluate(
        (
            VerificationResult(
                name="pytest",
                status=VerificationStatus.PASSED,
                message="All tests passed",
            ),
        )
    )

    execution = orchestrator.complete(execution, verification)
    assert execution.state.status == HarnessExecutionStatus.COMPLETED


def test_orchestrator_rejects_completion_when_verification_fails() -> None:
    orchestrator, execution = create_execution()

    execution = orchestrator.start(execution)
    execution = orchestrator.begin_verification(execution)

    verification = VerificationEngine().evaluate(
        (
            VerificationResult(
                name="pytest",
                status=VerificationStatus.FAILED,
                message="Tests failed",
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="Execution cannot be completed until verification passes",
    ):
        orchestrator.complete(execution, verification)


def test_orchestrator_rejects_completion_without_verification() -> None:
    orchestrator, execution = create_execution()

    execution = orchestrator.start(execution)
    execution = orchestrator.begin_verification(execution)

    with pytest.raises(
        ValueError,
        match="Execution cannot be completed until verification passes",
    ):
        orchestrator.complete(execution)


def test_orchestrator_can_fail_execution() -> None:
    orchestrator, execution = create_execution()

    execution = orchestrator.start(execution)
    failed_execution = orchestrator.fail(execution)

    assert execution.state.status == HarnessExecutionStatus.RUNNING
    assert failed_execution.state.status == HarnessExecutionStatus.FAILED


def test_orchestrator_preserves_execution_context_during_transition() -> None:
    orchestrator, execution = create_execution()

    started = orchestrator.start(execution)

    assert started.context == execution.context
    assert started.instructions == execution.instructions
    assert started.policy == execution.policy
    assert started.state.task_id == execution.state.task_id
