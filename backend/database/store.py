from __future__ import annotations
import json, sqlite3
from pathlib import Path

class BattleStore:
    def __init__(self, path: str = "data/agentwar.db"):
        db = Path(path); db.parent.mkdir(parents=True, exist_ok=True)
        self.path = str(db)
        with self._connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS rounds (id INTEGER PRIMARY KEY AUTOINCREMENT, battle_id TEXT, round_no INTEGER, payload TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, battle_id TEXT, kind TEXT, payload TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def _connect(self):
        return sqlite3.connect(self.path)

    def save_round(self, battle_id: str, round_no: int, payload: dict):
        with self._connect() as conn:
            conn.execute("INSERT INTO rounds(battle_id, round_no, payload) VALUES(?,?,?)", (battle_id, round_no, json.dumps(payload)))

    def add_event(self, battle_id: str, kind: str, payload: dict):
        with self._connect() as conn:
            conn.execute("INSERT INTO events(battle_id, kind, payload) VALUES(?,?,?)", (battle_id, kind, json.dumps(payload)))

    def history(self, battle_id: str, limit: int = 20) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute("SELECT payload FROM rounds WHERE battle_id=? ORDER BY id DESC LIMIT ?", (battle_id, limit)).fetchall()
        return [json.loads(row[0]) for row in reversed(rows)]
