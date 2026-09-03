from dataclasses import dataclass


@dataclass(frozen=True)
class HarnessInstructions:
    system: str
    task: str

    def render(self) -> str:
        return f"{self.system}\n\nTask:\n{self.task}"
