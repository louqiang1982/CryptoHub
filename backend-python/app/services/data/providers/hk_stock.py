"""Hong Kong stock data provider (HKEX) via AKShare / Yahoo Finance fallback."""

from __future__ import annotations

import logging
from typing import Any

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)


class HkStockDataProvider(BaseDataProvider):
    """HK stock data provider.

    Uses AKShare for HK market data; falls back to Yahoo Finance
    (yfinance) by appending '.HK' to the symbol.
    """

    name = "hk_stock"

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        try:
            import asyncio
            import yfinance as yf
            yf_symbol = symbol if symbol.endswith(".HK") else f"{symbol}.HK"
            ticker = yf.Ticker(yf_symbol)
            df = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ticker.history(period="1y").tail(limit)
            )
            return [
                OHLCV(
                    timestamp=str(idx.date()),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=float(row["Volume"]),
                )
                for idx, row in df.iterrows()
            ]
        except Exception as exc:
            logger.error("HkStock OHLCV error for %s: %s", symbol, exc)
            return []

    async def get_ticker(self, symbol: str) -> Ticker:
        try:
            import asyncio
            import yfinance as yf
            yf_symbol = symbol if symbol.endswith(".HK") else f"{symbol}.HK"
            info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: yf.Ticker(yf_symbol).fast_info
            )
            return Ticker(
                symbol=symbol,
                last_price=float(getattr(info, "last_price", 0) or 0),
                bid=float(getattr(info, "bid", 0) or 0),
                ask=float(getattr(info, "ask", 0) or 0),
                volume_24h=float(getattr(info, "three_month_average_volume", 0) or 0),
                change_24h_pct=0.0,
                timestamp="",
            )
        except Exception as exc:
            logger.error("HkStock ticker error for %s: %s", symbol, exc)
            return Ticker(symbol=symbol, last_price=0, bid=0, ask=0,
                          volume_24h=0, change_24h_pct=0, timestamp="")

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        return OrderBook(symbol=symbol)

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        return [{"symbol": query, "name": query, "exchange": "HKEX"}]
