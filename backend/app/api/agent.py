from uuid import uuid4

from fastapi import APIRouter

from app.schemas.agent import AgentTaskRequest, AgentTaskResponse

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


@router.post("/tasks", response_model=AgentTaskResponse)
async def create_agent_task(
    request: AgentTaskRequest,
) -> AgentTaskResponse:
    return AgentTaskResponse(
        task_id=str(uuid4()),
        instruction=request.instruction,
        workspace=request.workspace,
        status="created",
    )
