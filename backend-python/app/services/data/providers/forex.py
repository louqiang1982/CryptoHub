"""Forex data provider – uses exchangerate.host (free) and Yahoo Finance as fallback."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

# Common forex pairs for quick lookup
MAJOR_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
    "AUD/USD", "NZD/USD", "USD/CAD",
]


class ForexDataProvider(BaseDataProvider):
    """Foreign exchange data provider."""

    name = "forex"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        # Use Yahoo Finance for historical forex data
        # symbol format: EUR/USD → EURUSD=X
        yahoo_sym = symbol.replace("/", "") + "=X"
        interval_map = {"1H": "60m", "4H": "60m", "1D": "1d", "1W": "1wk"}
        interval = interval_map.get(timeframe, "1d")
        range_map = {"60m": "5d", "1d": "1y", "1wk": "5y"}
        chart_range = range_map.get(interval, "1y")

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}"
        params = {"interval": interval, "range": chart_range}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        result_data = data.get("chart", {}).get("result", [{}])[0]
        timestamps = result_data.get("timestamp", [])
        quote = result_data.get("indicators", {}).get("quote", [{}])[0]

        bars: list[OHLCV] = []
        for i, ts in enumerate(timestamps[-limit:]):
            bars.append(
                OHLCV(
                    timestamp=str(ts),
                    open=float(quote.get("open", [0])[i] or 0),
                    high=float(quote.get("high", [0])[i] or 0),
                    low=float(quote.get("low", [0])[i] or 0),
                    close=float(quote.get("close", [0])[i] or 0),
                    volume=float(quote.get("volume", [0])[i] or 0),
                )
            )
        return bars

    async def get_ticker(self, symbol: str) -> Ticker:
        yahoo_sym = symbol.replace("/", "") + "=X"
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_sym}"
        params = {"interval": "1d", "range": "1d"}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
        price = float(meta.get("regularMarketPrice", 0))
        prev = float(meta.get("chartPreviousClose", 0))
        change = ((price - prev) / prev * 100.0) if prev else 0.0

        return Ticker(
            symbol=symbol,
            last_price=price,
            bid=price,
            ask=price,
            volume_24h=0.0,
            change_24h_pct=change,
            timestamp=str(meta.get("regularMarketTime", "")),
        )

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        return OrderBook(symbol=symbol, bids=[], asks=[], timestamp="")

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        q = query.upper()
        results: list[dict[str, Any]] = []
        for pair in MAJOR_PAIRS:
            if q in pair:
                results.append({"symbol": pair, "type": "forex", "exchange": "FX"})
        return results
