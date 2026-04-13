"""Strategy state snapshot for persistence/recovery."""

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class StrategySnapshot:
    """Capture and restore strategy state."""

    def __init__(self, strategy_id: str):
        self.strategy_id = strategy_id
        self.state: dict[str, Any] = {}
        self.timestamp: str = ""

    def capture(self, position: float, orders: list[dict], variables: dict[str, Any]) -> dict:
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.state = {
            "strategy_id": self.strategy_id,
            "timestamp": self.timestamp,
            "position": position,
            "pending_orders": orders,
            "variables": variables,
        }
        return self.state

    def serialize(self) -> str:
        return json.dumps(self.state, default=str)

    @classmethod
    def deserialize(cls, data: str) -> "StrategySnapshot":
        parsed = json.loads(data)
        snapshot = cls(parsed["strategy_id"])
        snapshot.state = parsed
        snapshot.timestamp = parsed.get("timestamp", "")
        return snapshot

    def restore(self) -> dict[str, Any]:
        return {
            "position": self.state.get("position", 0.0),
            "pending_orders": self.state.get("pending_orders", []),
            "variables": self.state.get("variables", {}),
        }
