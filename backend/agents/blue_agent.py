class BlueAgent:
    status = "READY"

    def analyze(self, telemetry, state):
        signal = telemetry.get("signal")
        responses = {
            "network_probe": ("Network probe detected; isolate simulated source", "contain"),
            "web_anomaly": ("Web anomaly detected; apply simulated rate limit", "rate_limit"),
            "auth_anomaly": ("Authentication anomaly detected; apply simulated lockout", "lockout"),
        }
        label, action = responses.get(signal, ("Observe telemetry", "observe"))
        return {"label": label, "action": action, "detected": signal in responses, "confidence": telemetry.get("confidence", 0.0)}
