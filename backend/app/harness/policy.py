from dataclasses import dataclass


@dataclass(frozen=True)
class HarnessPolicy:
    workspace_scope: str
    require_approval: bool = False
    require_verification: bool = True
