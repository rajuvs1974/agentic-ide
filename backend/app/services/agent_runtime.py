from app.models.agent import (
    AgentExecutionResult,
    AgentTask,
    AgentTaskStatus,
)


class AgentRuntime:
    async def execute(self, task: AgentTask) -> AgentExecutionResult:
        return AgentExecutionResult(
            task_id=task.task_id,
            status=AgentTaskStatus.COMPLETED,
            message=f"Task accepted: {task.instruction}",
        )
