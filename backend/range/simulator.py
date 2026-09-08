from __future__ import annotations
from datetime import datetime, timezone

SIMULATIONS = [
    {"id": "recon_burst", "signal": "scan", "severity": 2},
    {"id": "web_probe", "signal": "web_probe", "severity": 3},
    {"id": "auth_noise", "signal": "auth_anomaly", "severity": 3},
]

PLAYBOOKS = [
    {"id": "observe_scan", "signals": ["scan"], "response": "rate_limit"},
    {"id": "contain_web", "signals": ["web_probe"], "response": "isolate_service"},
    {"id": "protect_auth", "signals": ["auth_anomaly"], "response": "temporary_lock"},
]

def run_simulation(simulation_id: str) -> dict:
    sim = next(s for s in SIMULATIONS if s["id"] == simulation_id)
    return {"simulation": simulation_id, "signal": sim["signal"], "severity": sim["severity"], "timestamp": datetime.now(timezone.utc).isoformat(), "isolated": True}

def apply_response(playbook_id: str, telemetry: dict) -> dict:
    pb = next(p for p in PLAYBOOKS if p["id"] == playbook_id)
    matched = telemetry.get("signal") in pb["signals"]
    return {"playbook": playbook_id, "response": pb["response"], "matched": matched, "contained": matched}
