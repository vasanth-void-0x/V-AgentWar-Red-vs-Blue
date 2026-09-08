# V-AgentWar Roadmap

## Phase 1 — Functional battle loop
- [x] V-Core state/orchestrator
- [x] Controlled Red simulation catalog
- [x] Blue analysis/response abstraction
- [x] Judge scoring
- [x] API + dashboard scaffold
- [x] Isolated Docker range scaffold

## Phase 2 — Real telemetry
- [ ] Range event collector
- [ ] Blue detection adapters
- [ ] WebSocket push event bus
- [ ] Persistent SQLite battle history

## Phase 3 — Intelligence
- [ ] Local/free LLM adapter
- [ ] Structured planner outputs
- [ ] RAG knowledge base for defensive playbooks and permitted simulation descriptions
- [ ] Cross-round battle memory
- [ ] Verifier/re-plan loop

## Phase 4 — MCP
- [ ] MCP capability registry
- [ ] Per-agent permission policy
- [ ] Audit log for every tool call
- [ ] Human approval for higher-risk lab actions

## Phase 5 — Evaluation
- [ ] Detection rate
- [ ] Time-to-detect
- [ ] Containment success
- [ ] False-positive metric
- [ ] Adaptation score

## Safety invariant
All Red actions remain predefined, capability-scoped, and restricted to the disposable isolated range. No arbitrary payload execution or external targeting.
