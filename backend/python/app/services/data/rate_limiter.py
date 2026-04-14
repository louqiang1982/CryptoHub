"""Token-bucket rate limiter for data provider API calls."""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RateLimiterConfig:
    """Configuration for a single rate-limit bucket."""

    rate: float  # requests per second
    burst: int = 1  # max burst size (token bucket capacity)


class TokenBucketLimiter:
    """Async token-bucket rate limiter.

    Parameters
    ----------
    rate:
        Refill rate in tokens (requests) per second.
    burst:
        Maximum number of tokens that can accumulate.
    """

    def __init__(self, rate: float, burst: int = 1) -> None:
        self._rate = rate
        self._burst = float(burst)
        self._tokens = float(burst)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        """Block until *tokens* tokens are available."""
        async with self._lock:
            await self._wait_for_tokens(tokens)

    async def _wait_for_tokens(self, tokens: float) -> None:
        while True:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return
            # Calculate wait time
            deficit = tokens - self._tokens
            wait = deficit / self._rate
            await asyncio.sleep(wait)

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._burst, self._tokens + elapsed * self._rate)
        self._last_refill = now

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """Non-blocking attempt to acquire tokens.  Returns False if unavailable."""
        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False


class RateLimiterRegistry:
    """Registry of per-provider rate limiters."""

    _DEFAULT_CONFIGS: dict[str, RateLimiterConfig] = {
        "binance": RateLimiterConfig(rate=10.0, burst=20),
        "okx": RateLimiterConfig(rate=5.0, burst=10),
        "bybit": RateLimiterConfig(rate=5.0, burst=10),
        "coinbase": RateLimiterConfig(rate=3.0, burst=6),
        "kraken": RateLimiterConfig(rate=1.0, burst=3),
        "kucoin": RateLimiterConfig(rate=3.0, burst=6),
        "yfinance": RateLimiterConfig(rate=2.0, burst=5),
        "polymarket": RateLimiterConfig(rate=2.0, burst=5),
        "tencent": RateLimiterConfig(rate=5.0, burst=10),
        "default": RateLimiterConfig(rate=2.0, burst=4),
    }

    def __init__(self) -> None:
        self._limiters: dict[str, TokenBucketLimiter] = {}

    def get(self, provider: str) -> TokenBucketLimiter:
        key = provider.lower()
        if key not in self._limiters:
            cfg = self._DEFAULT_CONFIGS.get(key, self._DEFAULT_CONFIGS["default"])
            self._limiters[key] = TokenBucketLimiter(rate=cfg.rate, burst=cfg.burst)
        return self._limiters[key]

    async def acquire(self, provider: str) -> None:
        """Convenience: acquire one token for *provider*."""
        await self.get(provider).acquire()

    def configure(self, provider: str, rate: float, burst: int = 1) -> None:
        """Override defaults for a specific provider."""
        key = provider.lower()
        self._limiters[key] = TokenBucketLimiter(rate=rate, burst=burst)


# Module-level singleton
rate_limiter_registry = RateLimiterRegistry()
