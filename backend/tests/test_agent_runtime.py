import pytest

from app.models.agent import AgentTask, AgentTaskStatus
from app.services.agent_runtime import AgentRuntime


@pytest.mark.anyio
async def test_agent_runtime_executes_task() -> None:
    runtime = AgentRuntime()

    task = AgentTask(
        task_id="test-task",
        instruction="Create a health endpoint",
        workspace="/workspace/demo",
    )

    result = await runtime.execute(task)

    assert result.task_id == "test-task"
    assert result.status == AgentTaskStatus.COMPLETED
    assert "Create a health endpoint" in result.message
