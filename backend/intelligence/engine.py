from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class Decision:
    action: str
    reason: str
    confidence: float

class IntelligenceEngine:
    """Local-first deterministic planner with optional LLM adapters later.

    Keeps the MVP runnable without paid APIs. It reasons only over the
    controlled simulation catalogue supplied by V-Core.
    """
    def choose_red(self, allowed: list[dict[str, Any]], history: list[dict[str, Any]]) -> Decision:
        tried = {h.get("red_action") for h in history[-5:]}
        candidate = next((a for a in allowed if a["id"] not in tried), allowed[0])
        return Decision(candidate["id"], "Prefer an allowed simulation not used recently", 0.82)

    def choose_blue(self, telemetry: dict[str, Any], playbooks: list[dict[str, Any]]) -> Decision:
        signal = telemetry.get("signal", "unknown")
        candidate = next((p for p in playbooks if signal in p.get("signals", [])), playbooks[0])
        return Decision(candidate["id"], f"Playbook matched telemetry signal: {signal}", 0.88)
