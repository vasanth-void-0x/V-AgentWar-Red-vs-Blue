from __future__ import annotations
import uuid
from backend.database.store import BattleStore
from backend.intelligence.engine import IntelligenceEngine
from backend.range.simulator import SIMULATIONS, PLAYBOOKS, run_simulation, apply_response

class BattleEngine:
    def __init__(self, store: BattleStore | None = None):
        self.store = store or BattleStore()
        self.ai = IntelligenceEngine()

    def create(self) -> dict:
        return {"battle_id": uuid.uuid4().hex[:10], "round": 0, "red_score": 0, "blue_score": 0, "status": "ready"}

    def run_round(self, state: dict) -> dict:
        battle_id = state["battle_id"]
        history = self.store.history(battle_id)
        red = self.ai.choose_red(SIMULATIONS, history)
        telemetry = run_simulation(red.action)
        blue = self.ai.choose_blue(telemetry, PLAYBOOKS)
        defense = apply_response(blue.action, telemetry)
        red_points = 25 if not defense["contained"] else 8
        blue_points = 25 if defense["contained"] else 5
        round_no = int(state.get("round", 0)) + 1
        result = {
            "battle_id": battle_id, "round": round_no,
            "red_action": red.action, "red_reason": red.reason,
            "telemetry": telemetry,
            "blue_action": blue.action, "blue_reason": blue.reason,
            "defense": defense,
            "red_points": red_points, "blue_points": blue_points,
            "red_score": int(state.get("red_score", 0)) + red_points,
            "blue_score": int(state.get("blue_score", 0)) + blue_points,
            "status": "round_complete",
            "adapted": bool(history),
        }
        self.store.save_round(battle_id, round_no, result)
        return result
