from dataclasses import dataclass, field


@dataclass(frozen=True)
class HarnessContext:
    task_id: str
    workspace: str
    instruction: str
    environment: str = "development"
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    state: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, str] = field(default_factory=dict)
