class JudgeAgent:
    status = "READY"

    def evaluate(self, red_action, telemetry, blue_action):
        detected = bool(blue_action.get("detected"))
        red_points = 3 if not detected else 1
        blue_points = 3 if detected else 0
        return {
            "red_points": red_points,
            "blue_points": blue_points,
            "detected": detected,
            "contained": detected and blue_action.get("action") != "observe",
            "summary": "Blue contained the simulated event" if detected else "Red simulation evaded detection",
        }
