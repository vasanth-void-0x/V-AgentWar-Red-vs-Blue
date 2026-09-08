class RedAgent:
    """Selects only predefined, non-destructive simulations for the isolated range."""
    status = "READY"
    catalog = [
        {"id": "service-probe", "label": "Controlled service discovery simulation", "severity": "low"},
        {"id": "web-probe", "label": "Controlled web probe simulation", "severity": "medium"},
        {"id": "auth-noise", "label": "Synthetic authentication anomaly", "severity": "medium"},
    ]

    def choose(self, state):
        # Deterministic adaptation for MVP: avoid repeating the immediately previous strategy.
        previous = state.memory[-1]["red"]["id"] if state.memory else None
        choices = [x for x in self.catalog if x["id"] != previous] or self.catalog
        return choices[state.round % len(choices)]

    def simulate(self, action):
        telemetry = {
            "service-probe": {"signal": "network_probe", "confidence": 0.86},
            "web-probe": {"signal": "web_anomaly", "confidence": 0.91},
            "auth-noise": {"signal": "auth_anomaly", "confidence": 0.88},
        }[action["id"]]
        return {**telemetry, "simulation_id": action["id"], "summary": f"Synthetic telemetry generated: {telemetry['signal']}"}
