"""Stock market data provider using public APIs."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

_YAHOO_BASE = "https://query1.finance.yahoo.com/v8/finance"


class StockDataProvider(BaseDataProvider):
    """Fetch equity/stock data via public Yahoo Finance endpoints."""

    name = "stock"

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        interval_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1H": "60m",
            "1D": "1d",
            "1W": "1wk",
        }
        interval = interval_map.get(timeframe, "1d")
        range_map = {
            "1m": "1d",
            "5m": "5d",
            "15m": "5d",
            "30m": "5d",
            "60m": "1mo",
            "1d": "1y",
            "1wk": "5y",
        }
        chart_range = range_map.get(interval, "1y")

        url = f"{_YAHOO_BASE}/chart/{symbol}"
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
        url = f"{_YAHOO_BASE}/chart/{symbol}"
        params = {"interval": "1d", "range": "1d"}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
        price = float(meta.get("regularMarketPrice", 0))
        prev_close = float(meta.get("chartPreviousClose", 0))
        change_pct = ((price - prev_close) / prev_close * 100.0) if prev_close else 0.0

        return Ticker(
            symbol=symbol,
            last_price=price,
            bid=price,
            ask=price,
            volume_24h=float(meta.get("regularMarketVolume", 0)),
            change_24h_pct=change_pct,
            timestamp=str(meta.get("regularMarketTime", "")),
        )

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        # Stocks generally don't expose public L2 order books
        return OrderBook(symbol=symbol, bids=[], asks=[], timestamp="")

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        params = {"q": query, "quotesCount": 20, "newsCount": 0}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        return [
            {
                "symbol": item.get("symbol"),
                "name": item.get("shortname"),
                "exchange": item.get("exchange"),
                "type": item.get("quoteType", "equity"),
            }
            for item in data.get("quotes", [])
        ]
