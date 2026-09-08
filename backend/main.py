import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.core.battle_engine import BattleEngine

app = FastAPI(
    title=f"{settings.app_name} API",
    version="0.3.0",
    debug=settings.debug,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = BattleEngine()
state = engine.create()
subscribers: set[WebSocket] = set()


class RoundRequest(BaseModel):
    rounds: int = 1


async def broadcast(payload: dict):
    dead = []
    for ws in subscribers:
        try:
            await ws.send_json(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        subscribers.discard(ws)


@app.get("/health")
def health():
    return {
        "status": "online",
        "app": settings.app_name,
        "environment": settings.app_env,
        "engine": "V-Core",
        "safe_mode": settings.vcore_safe_mode,
        "mode": "isolated-controlled-range",
        "features": {
            "llm": settings.llm_enabled,
            "rag": settings.rag_enabled,
            "mcp": settings.mcp_enabled,
            "cyber_range": settings.cyber_range_enabled,
        },
    }


@app.get("/api/state")
def get_state():
    return state


@app.post("/api/battle/reset")
def reset():
    global state
    state = engine.create()
    return state


@app.post("/api/battle/start")
async def start(req: RoundRequest):
    global state
    rounds = max(1, min(req.rounds, settings.vcore_max_rounds))
    results = []
    for _ in range(rounds):
        state = engine.run_round(state)
        results.append(state)
        await broadcast({"type": "round_complete", "data": state})
        await asyncio.sleep(0.05)
    return {"state": state, "rounds": results}


@app.websocket("/ws/events")
async def events(ws: WebSocket):
    await ws.accept()
    subscribers.add(ws)
    await ws.send_json({"type": "state", "data": state})
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        subscribers.discard(ws)
