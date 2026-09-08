from dataclasses import asdict
from datetime import datetime, timezone
from core.state import BattleState
from agents.red_agent import RedAgent
from agents.blue_agent import BlueAgent
from agents.judge_agent import JudgeAgent

class VCore:
    def __init__(self):
        self.red = RedAgent()
        self.blue = BlueAgent()
        self.judge = JudgeAgent()
        self.state = BattleState()
        self.events = []

    def emit(self, actor, kind, message, data=None):
        event = {"time": datetime.now(timezone.utc).isoformat(), "actor": actor, "kind": kind, "message": message, "data": data or {}}
        self.events.append(event)
        return event

    def run_round(self):
        self.state.round += 1
        self.state.status = "ACTIVE"
        self.emit("V-CORE", "round", f"Round {self.state.round} started")

        red_action = self.red.choose(self.state)
        self.emit("RED", "simulation", red_action["label"], red_action)

        telemetry = self.red.simulate(red_action)
        self.emit("RANGE", "telemetry", telemetry["summary"], telemetry)

        blue_action = self.blue.analyze(telemetry, self.state)
        self.emit("BLUE", "response", blue_action["label"], blue_action)

        verdict = self.judge.evaluate(red_action, telemetry, blue_action)
        self.state.red_score += verdict["red_points"]
        self.state.blue_score += verdict["blue_points"]
        self.state.last_verdict = verdict
        self.state.memory.append({"round": self.state.round, "red": red_action, "blue": blue_action, "verdict": verdict})
        self.emit("JUDGE", "verdict", verdict["summary"], verdict)
        self.state.status = "IDLE"
        return verdict

    def run(self, rounds=1):
        verdicts = [self.run_round() for _ in range(rounds)]
        return {"state": self.snapshot(), "verdicts": verdicts, "events": self.events[-20:]}

    def snapshot(self):
        return asdict(self.state) | {"vcore": "ONLINE", "red": self.red.status, "blue": self.blue.status}

    def reset(self):
        self.state = BattleState()
        self.events = []
