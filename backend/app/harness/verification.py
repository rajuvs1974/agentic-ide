from dataclasses import dataclass
from enum import StrEnum


class VerificationStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True)
class VerificationResult:
    name: str
    status: VerificationStatus
    message: str

    @property
    def passed(self) -> bool:
        return self.status == VerificationStatus.PASSED
