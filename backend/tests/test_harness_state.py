from app.harness.state import HarnessExecutionStatus, HarnessState


def test_harness_state_defaults_to_created() -> None:
    state = HarnessState(task_id="task-123")

    assert state.task_id == "task-123"
    assert state.status == HarnessExecutionStatus.CREATED


def test_harness_state_supports_execution_status() -> None:
    state = HarnessState(
        task_id="task-456",
        status=HarnessExecutionStatus.RUNNING,
    )

    assert state.task_id == "task-456"
    assert state.status == HarnessExecutionStatus.RUNNING


def test_harness_execution_status_contains_expected_lifecycle() -> None:
    assert HarnessExecutionStatus.CREATED.value == "created"
    assert HarnessExecutionStatus.RUNNING.value == "running"
    assert HarnessExecutionStatus.TOOL_CALL.value == "tool_call"
    assert HarnessExecutionStatus.VERIFYING.value == "verifying"
    assert HarnessExecutionStatus.COMPLETED.value == "completed"
    assert HarnessExecutionStatus.FAILED.value == "failed"
