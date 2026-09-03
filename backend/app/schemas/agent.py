from pydantic import BaseModel, Field


class AgentTaskRequest(BaseModel):
    instruction: str = Field(min_length=1)
    workspace: str = Field(min_length=1)


class AgentTaskResponse(BaseModel):
    task_id: str
    instruction: str
    workspace: str
    status: str
