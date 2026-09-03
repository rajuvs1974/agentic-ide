from app.harness.tool_registry import ToolDefinition, ToolRegistry


def test_tool_registry_registers_and_discovers_tool() -> None:
    registry = ToolRegistry()

    tool = ToolDefinition(
        name="filesystem",
        description="Read and write files in the workspace",
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
    )
    terminal = ToolDefinition(
        name="terminal",
        description="Execute approved terminal commands",
    )

    registry.register(filesystem)
    registry.register(terminal)

    assert registry.list_tools() == (filesystem, terminal)
