"""In-memory and Redis-backed cache manager for market data."""

from __future__ import annotations

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Simple TTL-based in-process cache."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}  # key → (value, expiry)

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expiry = entry
        if expiry > 0 and time.monotonic() > expiry:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        expiry = time.monotonic() + ttl if ttl > 0 else 0
        self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        return len(self._store)


class CacheManager:
    """Two-level cache: in-memory L1 + optional Redis L2."""

    def __init__(
        self,
        redis_client: Any = None,
        l1_ttl: int = 10,
        l2_ttl: int = 300,
    ) -> None:
        self._l1 = InMemoryCache()
        self._redis = redis_client
        self._l1_ttl = l1_ttl
        self._l2_ttl = l2_ttl

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def get(self, key: str) -> Any | None:
        # L1 hit
        value = self._l1.get(key)
        if value is not None:
            return value

        # L2 hit
        if self._redis is not None:
            try:
                raw = await self._redis.get(key)
                if raw is not None:
                    value = json.loads(raw)
                    self._l1.set(key, value, ttl=self._l1_ttl)
                    return value
            except Exception as exc:
                logger.warning("Redis GET error for key %s: %s", key, exc)

        return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        l2_ttl = ttl if ttl is not None else self._l2_ttl
        self._l1.set(key, value, ttl=min(self._l1_ttl, l2_ttl))

        if self._redis is not None:
            try:
                await self._redis.set(key, json.dumps(value), ex=l2_ttl)
            except Exception as exc:
                logger.warning("Redis SET error for key %s: %s", key, exc)

    async def delete(self, key: str) -> None:
        self._l1.delete(key)
        if self._redis is not None:
            try:
                await self._redis.delete(key)
            except Exception as exc:
                logger.warning("Redis DELETE error: %s", exc)

    async def get_or_fetch(
        self,
        key: str,
        fetch_fn: Any,
        ttl: int | None = None,
    ) -> Any:
        """Return cached value or call *fetch_fn* and cache the result."""
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = await fetch_fn()
        if value is not None:
            await self.set(key, value, ttl=ttl)
        return value
