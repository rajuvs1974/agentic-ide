from app.harness.tool_execution import (
    ToolExecutionStatus,
    ToolRequest,
    ToolResult,
)


def test_tool_request_contains_tool_and_arguments() -> None:
    request = ToolRequest(
        tool_name="filesystem.read_file",
        arguments={"path": "README.md"},
    )

    assert request.tool_name == "filesystem.read_file"
    assert request.arguments == {"path": "README.md"}


def test_successful_tool_result() -> None:
    result = ToolResult(
        tool_name="filesystem.read_file",
        status=ToolExecutionStatus.SUCCESS,
        output="file contents",
    )

    assert result.succeeded is True
    assert result.output == "file contents"
    assert result.error is None


def test_failed_tool_result() -> None:
    result = ToolResult(
        tool_name="filesystem.read_file",
        status=ToolExecutionStatus.FAILED,
        error="File not found",
    )

    assert result.succeeded is False
    assert result.output is None
    assert result.error == "File not found"