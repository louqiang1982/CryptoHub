"""Futures data provider via Yahoo Finance / CCXT.

Supports commodity futures (crude oil, gold, natural gas, etc.) as well
as index futures.  Uses Yahoo Finance for most futures (e.g. CL=F, GC=F)
and CCXT for crypto perpetuals/futures.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

# Common Yahoo Finance futures symbols
FUTURES_SYMBOLS = {
    "CL": "CL=F",   # Crude Oil
    "GC": "GC=F",   # Gold
    "SI": "SI=F",   # Silver
    "NG": "NG=F",   # Natural Gas
    "ZC": "ZC=F",   # Corn
    "ZW": "ZW=F",   # Wheat
    "ES": "ES=F",   # S&P 500 E-mini
    "NQ": "NQ=F",   # Nasdaq 100 E-mini
    "YM": "YM=F",   # Dow Jones E-mini
    "RTY": "RTY=F", # Russell 2000 E-mini
    "6E": "6E=F",   # Euro FX futures
    "6J": "6J=F",   # Japanese Yen futures
}


class FuturesDataProvider(BaseDataProvider):
    """Futures data provider using Yahoo Finance as primary source."""

    name = "futures"

    def _resolve_symbol(self, symbol: str) -> str:
        """Normalise a symbol to its Yahoo Finance equivalent."""
        upper = symbol.upper()
        return FUTURES_SYMBOLS.get(upper, upper if upper.endswith("=F") else f"{upper}=F")

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        try:
            import asyncio
            import yfinance as yf
            yf_symbol = self._resolve_symbol(symbol)
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
            logger.error("Futures OHLCV error for %s: %s", symbol, exc)
            return []

    async def get_ticker(self, symbol: str) -> Ticker:
        try:
            import asyncio
            import yfinance as yf
            yf_symbol = self._resolve_symbol(symbol)
            info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: yf.Ticker(yf_symbol).fast_info
            )
            last = float(getattr(info, "last_price", 0) or 0)
            return Ticker(
                symbol=symbol,
                last_price=last,
                bid=last,
                ask=last,
                volume_24h=float(getattr(info, "three_month_average_volume", 0) or 0),
                change_24h_pct=0.0,
                timestamp="",
            )
        except Exception as exc:
            logger.error("Futures ticker error for %s: %s", symbol, exc)
            return Ticker(symbol=symbol, last_price=0, bid=0, ask=0,
                          volume_24h=0, change_24h_pct=0, timestamp="")

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        return OrderBook(symbol=symbol)

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        results = [
            {"symbol": k, "name": f"{k} Futures ({v})", "exchange": "CME/CBOT"}
            for k, v in FUTURES_SYMBOLS.items()
            if query.upper() in k
        ]
        return results
