"""Cryptocurrency data provider using ccxt."""

from __future__ import annotations

import logging
from typing import Any

import ccxt.async_support as ccxt

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

# Map of human-readable timeframes to ccxt timeframe strings
TIMEFRAME_MAP: dict[str, str] = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1H": "1h",
    "4H": "4h",
    "1D": "1d",
    "1W": "1w",
}


class CryptoDataProvider(BaseDataProvider):
    """Fetch crypto market data via ccxt (default: Binance)."""

    name = "crypto"

    def __init__(self, exchange_id: str = "binance") -> None:
        exchange_class = getattr(ccxt, exchange_id, None)
        if exchange_class is None:
            raise ValueError(f"Unknown exchange: {exchange_id}")
        self.exchange: ccxt.Exchange = exchange_class({"enableRateLimit": True})

    async def close(self) -> None:
        await self.exchange.close()

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        tf = TIMEFRAME_MAP.get(timeframe, timeframe)
        raw = await self.exchange.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
        return [
            OHLCV(
                timestamp=self.exchange.iso8601(row[0]),
                open=float(row[1]),
                high=float(row[2]),
                low=float(row[3]),
                close=float(row[4]),
                volume=float(row[5]),
            )
            for row in raw
        ]

    async def get_ticker(self, symbol: str) -> Ticker:
        data = await self.exchange.fetch_ticker(symbol)
        return Ticker(
            symbol=symbol,
            last_price=float(data.get("last", 0)),
            bid=float(data.get("bid", 0)),
            ask=float(data.get("ask", 0)),
            volume_24h=float(data.get("quoteVolume", 0)),
            change_24h_pct=float(data.get("percentage", 0)),
            timestamp=data.get("datetime", ""),
        )

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        data = await self.exchange.fetch_order_book(symbol, limit=depth)
        return OrderBook(
            symbol=symbol,
            bids=data.get("bids", []),
            asks=data.get("asks", []),
            timestamp=data.get("datetime", ""),
        )

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        await self.exchange.load_markets()
        results: list[dict[str, Any]] = []
        q = query.upper()
        for market_id, market in self.exchange.markets.items():
            if q in market_id.upper():
                results.append(
                    {
                        "symbol": market["symbol"],
                        "base": market.get("base"),
                        "quote": market.get("quote"),
                        "exchange": self.exchange.id,
                        "type": market.get("type", "spot"),
                    }
                )
                if len(results) >= 20:
                    break
        return results
