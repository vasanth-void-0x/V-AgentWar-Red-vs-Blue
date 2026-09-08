from backend.core.battle_engine import BattleEngine
from backend.database.store import BattleStore

def test_battle_round(tmp_path):
    engine = BattleEngine(BattleStore(str(tmp_path / "test.db")))
    state = engine.create()
    result = engine.run_round(state)
    assert result["round"] == 1
    assert result["telemetry"]["isolated"] is True
    assert result["blue_score"] > 0

def test_agent_adapts_across_rounds(tmp_path):
    engine = BattleEngine(BattleStore(str(tmp_path / "test.db")))
    first = engine.run_round(engine.create())
    second = engine.run_round(first)
    assert second["round"] == 2
    assert second["adapted"] is True
    assert second["red_action"] != first["red_action"]
