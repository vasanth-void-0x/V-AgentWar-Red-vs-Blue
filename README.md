# V-AgentWar — RED vs BLUE

**Adaptive Multi-Agent Cyber Range powered by V-Core.**

V-AgentWar is a portfolio-oriented, isolated cyber-range project where a Red Agent selects controlled security simulations, a Blue Agent analyzes generated telemetry and applies permitted defensive responses, and a Judge scores each round. V-Core orchestrates state, memory, policy, and adaptation.

> Safety scope: Red capabilities are intentionally limited to predefined simulations inside the disposable lab. The project does not provide arbitrary exploitation or real-world targeting.

## Architecture

`V-Core → Red Agent / Blue Agent → Isolated Range → Judge → Memory → Next Round`

## MVP

- FastAPI backend
- V-Core round/state orchestration
- Red, Blue, and Judge agent abstractions
- Controlled simulation catalog
- Live battle event stream via WebSocket
- SQLite battle history
- React/Next.js dashboard scaffold
- Docker lab placeholder
- RAG/MCP extension points

## Status

Initial project scaffold. The first milestone is a deterministic end-to-end battle loop before adding LLM, RAG, MCP, and richer cyber-range integrations.
