from uuid import uuid4

from fastapi import APIRouter

from app.models.agent import AgentTask
from app.schemas.agent import AgentTaskRequest, AgentTaskResponse
from app.services.agent_runtime import AgentRuntime

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

runtime = AgentRuntime()


@router.post("/tasks", response_model=AgentTaskResponse)
async def create_agent_task(
    request: AgentTaskRequest,
) -> AgentTaskResponse:
    task = AgentTask(
        task_id=str(uuid4()),
        instruction=request.instruction,
        workspace=request.workspace,
    )

    result = await runtime.execute(task)

    return AgentTaskResponse(
        task_id=result.task_id,
        instruction=task.instruction,
        workspace=task.workspace,
        status=result.status.value,
    )