from dataclasses import dataclass

from app.harness.context import HarnessContext
from app.harness.instructions import HarnessInstructions
from app.harness.policy import HarnessPolicy
from app.harness.state import HarnessState


@dataclass(frozen=True)
class HarnessExecution:
    context: HarnessContext
    instructions: HarnessInstructions
    policy: HarnessPolicy
    state: HarnessState


class HarnessOrchestrator:
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
