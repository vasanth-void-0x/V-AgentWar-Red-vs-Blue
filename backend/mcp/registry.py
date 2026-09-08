from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Capability:
    name: str
    team: str
    handler: Callable[..., Any]

class CapabilityRegistry:
    """Allowlisted capability router used by V-Core and MCP adapters."""
    def __init__(self):
        self._items: dict[str, Capability] = {}

    def register(self, name: str, team: str, handler: Callable[..., Any]):
        self._items[name] = Capability(name, team, handler)

    def list_for(self, team: str) -> list[str]:
        return sorted(c.name for c in self._items.values() if c.team in (team, "shared"))

    def call(self, team: str, name: str, **kwargs):
        cap = self._items.get(name)
        if not cap or cap.team not in (team, "shared"):
            raise PermissionError(f"Capability '{name}' is not permitted for {team}")
        return cap.handler(**kwargs)
