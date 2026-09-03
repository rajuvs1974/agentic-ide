from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationResult:
    score: float
    passed: bool
    message: str
