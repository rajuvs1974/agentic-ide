from app.harness.instructions import HarnessInstructions


def test_harness_instructions_render_system_and_task() -> None:
    instructions = HarnessInstructions(
        system="You are an expert software engineering agent.",
        task="Fix the failing test.",
    )

    rendered = instructions.render()

    assert "You are an expert software engineering agent." in rendered
    assert "Task:" in rendered
    assert "Fix the failing test." in rendered


def test_harness_instructions_are_immutable() -> None:
    instructions = HarnessInstructions(
        system="Follow engineering standards.",
        task="Run the tests.",
    )

    assert instructions.system == "Follow engineering standards."
    assert instructions.task == "Run the tests."


def test_harness_instructions_preserve_multiline_content() -> None:
    instructions = HarnessInstructions(
        system="Follow these rules:\n1. Use type hints.\n2. Run tests.",
        task="Implement the endpoint.",
    )

    rendered = instructions.render()

    assert "1. Use type hints." in rendered
    assert "2. Run tests." in rendered
    assert "Implement the endpoint." in rendered
