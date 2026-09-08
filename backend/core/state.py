from dataclasses import dataclass, field
from typing import Any

@dataclass
class BattleState:
    round: int = 0
    status: str = "IDLE"
    red_score: int = 0
    blue_score: int = 0
    last_verdict: dict[str, Any] = field(default_factory=dict)
    memory: list[dict[str, Any]] = field(default_factory=list)
