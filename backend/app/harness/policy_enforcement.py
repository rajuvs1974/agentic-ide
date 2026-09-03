from app.harness.context import HarnessContext
from app.harness.policy import HarnessPolicy
from app.harness.tool_authorization import ToolAuthorization


class PolicyEnforcement:
    def __init__(
        self,
        authorization: ToolAuthorization,
        policy: HarnessPolicy,
    ) -> None:
        self._authorization = authorization
        self._policy = policy

    def can_use_tool(
        self,
        tool_name: str,
        context: HarnessContext,
    ) -> bool:
        if context.workspace != self._policy.workspace_scope:
            return False

        return self._authorization.is_authorized(tool_name, context)
