from dataclasses import dataclass

from app.harness.context import HarnessContext
from app.harness.instructions import HarnessInstructions
from app.harness.policy import HarnessPolicy
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.state import HarnessState


@dataclass(frozen=True)
class HarnessExecution:
    context: HarnessContext
    instructions: HarnessInstructions
    policy: HarnessPolicy
    state: HarnessState


class HarnessOrchestrator:
    def __init__(self, policy_enforcement: PolicyEnforcement) -> None:
        self._policy_enforcement = policy_enforcement

    def create_execution(
        self,
        context: HarnessContext,
        instructions: HarnessInstructions,
        policy: HarnessPolicy,
    ) -> HarnessExecution:
        state = HarnessState(task_id=context.task_id)

        return HarnessExecution(
            context=context,
            instructions=instructions,
            policy=policy,
            state=state,
        )

    def can_use_tool(
        self,
        execution: HarnessExecution,
        tool_name: str,
    ) -> bool:
        return self._policy_enforcement.can_use_tool(
            tool_name,
            execution.context,
        )
