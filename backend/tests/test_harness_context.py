from app.harness.context import HarnessContext


def test_harness_context_defaults() -> None:
    context = HarnessContext(
        task_id="task-123",
        workspace="/workspace/demo",
        instruction="Fix the failing test",
    )

    assert context.task_id == "task-123"
    assert context.workspace == "/workspace/demo"
    assert context.instruction == "Fix the failing test"
    assert context.environment == "development"
    assert context.allowed_tools == ()
    assert context.state == {}
    assert context.metadata == {}


def test_harness_context_supports_tools_and_metadata() -> None:
    context = HarnessContext(
        task_id="task-456",
        workspace="/workspace/demo",
        instruction="Run the tests",
        allowed_tools=("terminal", "filesystem"),
        state={"status": "running"},
        metadata={"source": "ide"},
    )

    assert context.allowed_tools == ("terminal", "filesystem")
    assert context.state["status"] == "running"
    assert context.metadata["source"] == "ide"
