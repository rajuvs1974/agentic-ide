from app.harness.tool_registry import ToolDefinition, ToolRegistry


def test_tool_registry_registers_and_discovers_tool() -> None:
    registry = ToolRegistry()

    tool = ToolDefinition(
    name="filesystem",
    description="Read and write workspace files",
    handler=lambda arguments: arguments,
)

    registry.register(tool)

    assert registry.get("filesystem") == tool
    assert registry.list_tools() == (tool,)


def test_tool_registry_returns_none_for_unknown_tool() -> None:
    registry = ToolRegistry()

    assert registry.get("unknown") is None


def test_tool_registry_supports_multiple_tools() -> None:
    registry = ToolRegistry()

    filesystem = ToolDefinition(
        name="filesystem",
        description="Read and write workspace files",
        handler=lambda arguments: arguments,
    )
    terminal = ToolDefinition(
        name="terminal",
        description="Execute approved terminal commands",
        handler=lambda arguments: arguments,
    )

    registry.register(filesystem)
    registry.register(terminal)

    assert registry.list_tools() == (filesystem, terminal)
