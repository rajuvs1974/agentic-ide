from app.harness.evaluation import EvaluationResult
from app.harness.evaluation_engine import EvaluationEngine


def test_evaluation_engine_calculates_average_score() -> None:
    engine = EvaluationEngine()

    results = (
        EvaluationResult(
            score=9.0,
            passed=True,
            message="Requirements satisfied",
        ),
        EvaluationResult(
            score=8.0,
            passed=True,
            message="Code quality is good",
        ),
    )

    summary = engine.evaluate(results)

    assert summary.results == results
    assert summary.score == 8.5
    assert summary.passed is True


def test_evaluation_engine_fails_below_passing_score() -> None:
    engine = EvaluationEngine()

    results = (
        EvaluationResult(
            score=5.0,
            passed=False,
            message="Requirements incomplete",
        ),
        EvaluationResult(
            score=6.0,
            passed=False,
            message="Additional work required",
        ),
    )

    summary = engine.evaluate(results)

    assert summary.score == 5.5
    assert summary.passed is False


def test_evaluation_engine_fails_when_no_results_exist() -> None:
    engine = EvaluationEngine()

    summary = engine.evaluate(())

    assert summary.results == ()
    assert summary.score == 0.0
    assert summary.passed is False


def test_evaluation_engine_supports_custom_passing_score() -> None:
    engine = EvaluationEngine()

    results = (
        EvaluationResult(
            score=8.0,
            passed=True,
            message="Good result",
        ),
    )

    summary = engine.evaluate(
        results,
        passing_score=9.0,
    )

    assert summary.score == 8.0
    assert summary.passed is False
