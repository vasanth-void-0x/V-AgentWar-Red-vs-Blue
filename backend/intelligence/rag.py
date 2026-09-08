from __future__ import annotations
import json
from pathlib import Path

class KnowledgeBase:
    def __init__(self, root: str = "knowledge"):
        self.root = Path(root)

    def retrieve(self, query: str, limit: int = 3) -> list[dict]:
        terms = set(query.lower().split())
        docs: list[tuple[int, dict]] = []
        if not self.root.exists():
            return []
        for path in self.root.rglob("*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            items = payload if isinstance(payload, list) else [payload]
            for item in items:
                text = json.dumps(item).lower()
                score = sum(1 for term in terms if term in text)
                if score:
                    docs.append((score, {**item, "source": str(path)}))
        docs.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in docs[:limit]]
