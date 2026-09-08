from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.vcore import VCore

app = FastAPI(title="V-AgentWar API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
core = VCore()

class BattleRequest(BaseModel):
    rounds: int = 1

@app.get("/health")
def health():
    return {"status": "online", "engine": "V-Core"}

@app.get("/api/state")
def state():
    return core.snapshot()

@app.post("/api/battle/start")
def start_battle(req: BattleRequest):
    return core.run(rounds=max(1, min(req.rounds, 10)))

@app.post("/api/battle/reset")
def reset_battle():
    core.reset()
    return core.snapshot()

@app.websocket("/ws/events")
async def events(ws: WebSocket):
    await ws.accept()
    try:
        for event in core.events[-50:]:
            await ws.send_json(event)
        while True:
            await ws.receive_text()
            for event in core.events[-10:]:
                await ws.send_json(event)
    except Exception:
        await ws.close()
