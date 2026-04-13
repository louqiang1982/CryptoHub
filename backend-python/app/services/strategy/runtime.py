"""Strategy runtime lifecycle manager."""

import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class StrategyState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"


class StrategyRuntime:
    """Manage strategy lifecycle."""

    def __init__(self) -> None:
        self._strategies: dict[str, StrategyState] = {}
        self._tasks: dict[str, asyncio.Task] = {}  # type: ignore[type-arg]

    async def start(self, strategy_id: str) -> bool:
        if strategy_id in self._strategies and self._strategies[strategy_id] == StrategyState.RUNNING:
            logger.warning("Strategy %s is already running", strategy_id)
            return False
        self._strategies[strategy_id] = StrategyState.RUNNING
        logger.info("Strategy %s started", strategy_id)
        return True

    async def stop(self, strategy_id: str) -> bool:
        if strategy_id not in self._strategies:
            return False
        if strategy_id in self._tasks:
            self._tasks[strategy_id].cancel()
            del self._tasks[strategy_id]
        self._strategies[strategy_id] = StrategyState.STOPPED
        logger.info("Strategy %s stopped", strategy_id)
        return True

    async def pause(self, strategy_id: str) -> bool:
        if self._strategies.get(strategy_id) != StrategyState.RUNNING:
            return False
        self._strategies[strategy_id] = StrategyState.PAUSED
        return True

    def get_state(self, strategy_id: str) -> StrategyState:
        return self._strategies.get(strategy_id, StrategyState.STOPPED)

    def list_running(self) -> list[str]:
        return [sid for sid, state in self._strategies.items() if state == StrategyState.RUNNING]


runtime = StrategyRuntime()
