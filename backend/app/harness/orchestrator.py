from dataclasses import dataclass

from app.harness.context import HarnessContext
from app.harness.instructions import HarnessInstructions
from app.harness.policy import HarnessPolicy
from app.harness.policy_enforcement import PolicyEnforcement
from app.harness.state import HarnessExecutionStatus, HarnessState
from app.harness.verification_engine import VerificationSummary


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

    def start(
        self,
        execution: HarnessExecution,
    ) -> HarnessExecution:
        return self._transition(
            execution,
            HarnessExecutionStatus.RUNNING,
        )

    def begin_tool_call(
        self,
        execution: HarnessExecution,
    ) -> HarnessExecution:
        return self._transition(
            execution,
            HarnessExecutionStatus.TOOL_CALL,
        )

    def begin_verification(
        self,
        execution: HarnessExecution,
    ) -> HarnessExecution:
        return self._transition(
            execution,
            HarnessExecutionStatus.VERIFYING,
        )

    def complete(
        self,
        execution: HarnessExecution,
        verification: VerificationSummary | None = None,
    ) -> HarnessExecution:
        if execution.policy.require_verification and (
            verification is None or not verification.passed
        ):
            raise ValueError(
                "Execution cannot be completed until verification passes"
            )

        return self._transition(
            execution,
            HarnessExecutionStatus.COMPLETED,
        )

    def fail(
        self,
        execution: HarnessExecution,
    ) -> HarnessExecution:
        return self._transition(
            execution,
            HarnessExecutionStatus.FAILED,
        )

    @staticmethod
    def _transition(
        execution: HarnessExecution,
        status: HarnessExecutionStatus,
    ) -> HarnessExecution:
        return HarnessExecution(
            context=execution.context,
            instructions=execution.instructions,
            policy=execution.policy,
            state=execution.state.transition(status),
        )
