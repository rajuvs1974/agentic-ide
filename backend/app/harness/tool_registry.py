from dataclasses import dataclass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition | None:
        return self._tools.get(name)

    def list_tools(self) -> tuple[ToolDefinition, ...]:
        return tuple(self._tools.values())
