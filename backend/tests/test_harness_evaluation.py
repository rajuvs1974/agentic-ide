from app.harness.evaluation import EvaluationResult


def test_evaluation_result_can_pass() -> None:
    result = EvaluationResult(
        score=9.0,
        passed=True,
        message="Task requirements were satisfied",
    )

    assert result.score == 9.0
    assert result.passed is True
    assert result.message == "Task requirements were satisfied"


def test_evaluation_result_can_fail() -> None:
    result = EvaluationResult(
        score=4.0,
        passed=False,
        message="Task requirements were not fully satisfied",
    )

    assert result.score == 4.0
    assert result.passed is False


def test_evaluation_result_supports_zero_score() -> None:
    result = EvaluationResult(
        score=0.0,
        passed=False,
        message="Task was not completed",
    )

    assert result.score == 0.0
    assert result.passed is False
