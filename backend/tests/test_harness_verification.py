from app.harness.verification import (
    VerificationResult,
    VerificationStatus,
)


def test_verification_result_can_pass() -> None:
    result = VerificationResult(
        name="pytest",
        status=VerificationStatus.PASSED,
        message="All tests passed",
    )

    assert result.name == "pytest"
    assert result.status == VerificationStatus.PASSED
    assert result.message == "All tests passed"
    assert result.passed is True


def test_verification_result_can_fail() -> None:
    result = VerificationResult(
        name="pytest",
        status=VerificationStatus.FAILED,
        message="One test failed",
    )

    assert result.status == VerificationStatus.FAILED
    assert result.passed is False


def test_verification_status_values() -> None:
    assert VerificationStatus.PASSED.value == "passed"
    assert VerificationStatus.FAILED.value == "failed"
