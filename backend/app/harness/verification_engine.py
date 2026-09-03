from dataclasses import dataclass

from app.harness.verification import VerificationResult


@dataclass(frozen=True)
class VerificationSummary:
    results: tuple[VerificationResult, ...]

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(result.passed for result in self.results)


class VerificationEngine:
    def evaluate(
        self,
        results: tuple[VerificationResult, ...],
    ) -> VerificationSummary:
        return VerificationSummary(results=results)
