"""Abstract base class for all market data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class OHLCV:
    """Single OHLCV bar."""

    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Ticker:
    """Real-time ticker snapshot."""

    symbol: str
    last_price: float
    bid: float
    ask: float
    volume_24h: float
    change_24h_pct: float
    timestamp: str


@dataclass
class OrderBook:
    """Top-of-book snapshot."""

    symbol: str
    bids: list[list[float]] = field(default_factory=list)
    asks: list[list[float]] = field(default_factory=list)
    timestamp: str = ""


class BaseDataProvider(ABC):
    """Interface every data provider must implement."""

    name: str = "base"

    @abstractmethod
    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        """Fetch historical OHLCV bars."""
        ...

    @abstractmethod
    async def get_ticker(self, symbol: str) -> Ticker:
        """Get real-time ticker for *symbol*."""
        ...

    @abstractmethod
    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        """Fetch order-book snapshot."""
        ...

    @abstractmethod
    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        """Search available symbols."""
        ...

    async def get_multiple_tickers(self, symbols: list[str]) -> list[Ticker]:
        """Convenience – fetch tickers for many symbols sequentially."""
        results: list[Ticker] = []
        for sym in symbols:
            try:
                results.append(await self.get_ticker(sym))
            except Exception:
                continue
        return results
