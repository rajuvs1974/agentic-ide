from app.harness.context import HarnessContext
from app.harness.tool_registry import ToolRegistry


class ToolAuthorization:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def is_authorized(
        self,
        tool_name: str,
        context: HarnessContext,
    ) -> bool:
        if self._registry.get(tool_name) is None:
            return False

        return tool_name in context.allowed_tools
