import pytest

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


def test_harness_state_supports_valid_transitions() -> None:
    state = HarnessState(task_id="task-123")

    state = state.transition(HarnessExecutionStatus.RUNNING)
    assert state.status == HarnessExecutionStatus.RUNNING

    state = state.transition(HarnessExecutionStatus.TOOL_CALL)
    assert state.status == HarnessExecutionStatus.TOOL_CALL

    state = state.transition(HarnessExecutionStatus.VERIFYING)
    assert state.status == HarnessExecutionStatus.VERIFYING

    state = state.transition(HarnessExecutionStatus.COMPLETED)
    assert state.status == HarnessExecutionStatus.COMPLETED


def test_harness_state_supports_failure_transition() -> None:
    state = HarnessState(
        task_id="task-123",
        status=HarnessExecutionStatus.RUNNING,
    )

    failed_state = state.transition(HarnessExecutionStatus.FAILED)

    assert state.status == HarnessExecutionStatus.RUNNING
    assert failed_state.status == HarnessExecutionStatus.FAILED


def test_harness_state_rejects_invalid_transition() -> None:
    state = HarnessState(task_id="task-123")

    with pytest.raises(ValueError, match="Invalid state transition"):
        state.transition(HarnessExecutionStatus.COMPLETED)


def test_completed_state_cannot_transition() -> None:
    state = HarnessState(
        task_id="task-123",
        status=HarnessExecutionStatus.COMPLETED,
    )

    with pytest.raises(ValueError, match="Invalid state transition"):
        state.transition(HarnessExecutionStatus.RUNNING)
