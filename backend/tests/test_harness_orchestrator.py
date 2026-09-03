from app.harness.context import HarnessContext
from app.harness.instructions import HarnessInstructions
from app.harness.orchestrator import HarnessOrchestrator
from app.harness.policy import HarnessPolicy
from app.harness.state import HarnessExecutionStatus


def test_orchestrator_creates_harness_execution() -> None:
    context = HarnessContext(
        task_id="task-123",
        workspace="/workspace/demo",
        instruction="Implement the health endpoint",
        allowed_tools=("filesystem", "terminal"),
    )

    instructions = HarnessInstructions(
        system="You are a software engineering agent.",
        task=context.instruction,
    )

    policy = HarnessPolicy(
        workspace_scope="/workspace/demo",
        require_verification=True,
    )

    orchestrator = HarnessOrchestrator()

    execution = orchestrator.create_execution(
        context=context,
        instructions=instructions,
        policy=policy,
    )

    assert execution.context == context
    assert execution.instructions == instructions
    assert execution.policy == policy
    assert execution.state.task_id == "task-123"
    assert execution.state.status == HarnessExecutionStatus.CREATED


def test_orchestrator_preserves_execution_configuration() -> None:
    context = HarnessContext(
        task_id="task-456",
        workspace="/workspace/project",
        instruction="Run the tests",
        allowed_tools=("terminal",),
    )

    instructions = HarnessInstructions(
        system="Follow engineering standards.",
        task="Run the tests",
    )

    policy = HarnessPolicy(
        workspace_scope="/workspace/project",
        require_approval=True,
        require_verification=True,
    )

    execution = HarnessOrchestrator().create_execution(
        context=context,
        instructions=instructions,
        policy=policy,
    )

    assert execution.context.workspace == "/workspace/project"
    assert execution.context.allowed_tools == ("terminal",)
    assert execution.instructions.system == "Follow engineering standards."
    assert execution.policy.require_approval is True
    assert execution.policy.require_verification is True
