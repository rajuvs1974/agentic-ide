from app.harness.verification import (
    VerificationResult,
    VerificationStatus,
)
from app.harness.verification_engine import VerificationEngine


def test_verification_engine_passes_when_all_checks_pass() -> None:
    engine = VerificationEngine()

    results = (
        VerificationResult(
            name="pytest",
            status=VerificationStatus.PASSED,
            message="All tests passed",
        ),
        VerificationResult(
            name="ruff",
            status=VerificationStatus.PASSED,
            message="No lint errors",
        ),
        VerificationResult(
            name="mypy",
            status=VerificationStatus.PASSED,
            message="No type errors",
        ),
    )

    summary = engine.evaluate(results)

    assert summary.results == results
    assert summary.passed is True


def test_verification_engine_fails_when_any_check_fails() -> None:
    engine = VerificationEngine()

    results = (
        VerificationResult(
            name="pytest",
            status=VerificationStatus.PASSED,
            message="All tests passed",
        ),
        VerificationResult(
            name="ruff",
            status=VerificationStatus.FAILED,
            message="Lint errors found",
        ),
    )

    summary = engine.evaluate(results)

    assert summary.passed is False


def test_verification_engine_fails_when_no_checks_exist() -> None:
    engine = VerificationEngine()

    summary = engine.evaluate(())

    assert summary.results == ()
    assert summary.passed is False
