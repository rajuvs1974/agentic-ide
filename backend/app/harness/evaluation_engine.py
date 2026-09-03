from dataclasses import dataclass

from app.harness.evaluation import EvaluationResult


@dataclass(frozen=True)
class EvaluationSummary:
    results: tuple[EvaluationResult, ...]
    score: float
    passed: bool


class EvaluationEngine:
    def evaluate(
        self,
        results: tuple[EvaluationResult, ...],
        passing_score: float = 7.0,
    ) -> EvaluationSummary:
        if not results:
            return EvaluationSummary(
                results=(),
                score=0.0,
                passed=False,
            )

        score = sum(result.score for result in results) / len(results)

        return EvaluationSummary(
            results=results,
            score=score,
            passed=score >= passing_score,
        )
