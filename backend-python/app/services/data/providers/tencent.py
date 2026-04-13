"""Tencent Finance quote provider (腾讯行情源).

Provides real-time and historical price data for A-shares, HK stocks and
major indices using Tencent's public finance API.  No API key required.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

TENCENT_REALTIME_URL = "https://qt.gtimg.cn/q={symbols}"
TENCENT_HIST_URL = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"


def _symbol_to_tencent(symbol: str) -> str:
    """Convert exchange:symbol notation to Tencent prefix notation."""
    sym = symbol.upper()
    if sym.startswith("SH") or sym.startswith("SZ") or sym.startswith("HK"):
        return sym.lower()
    # Guess exchange from code
    if sym.isdigit():
        return ("sh" if sym.startswith("6") else "sz") + sym
    return "hk" + sym.lstrip("0")


class TencentDataProvider(BaseDataProvider):
    """Real-time quote provider using the Tencent Finance (腾讯财经) API."""

    name = "tencent"

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=10.0,
            headers={
                "Referer": "https://finance.qq.com",
                "User-Agent": "Mozilla/5.0",
            },
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        tc_sym = _symbol_to_tencent(symbol)
        params = {
            "param": f"{tc_sym},day,,,{limit},,qfq",
            "_var": "kline_dayqfq",
        }
        try:
            resp = await self._client.get(TENCENT_HIST_URL, params=params)
            resp.raise_for_status()
            text = resp.text
            # Response is JS assignment, strip prefix
            json_start = text.index("{")
            import json
            data = json.loads(text[json_start:])
            day_data = (
                data.get("data", {})
                    .get(tc_sym, {})
                    .get("day", [])
            )
            return [
                OHLCV(
                    timestamp=row[0],
                    open=float(row[1]),
                    close=float(row[2]),
                    high=float(row[3]),
                    low=float(row[4]),
                    volume=float(row[5]),
                )
                for row in day_data
            ]
        except Exception as exc:
            logger.error("Tencent OHLCV error for %s: %s", symbol, exc)
            return []

    async def get_ticker(self, symbol: str) -> Ticker:
        tc_sym = _symbol_to_tencent(symbol)
        url = TENCENT_REALTIME_URL.format(symbols=tc_sym)
        try:
            resp = await self._client.get(url)
            resp.raise_for_status()
            # Format: v_sz000001="...~fields~..."
            text = resp.text.strip().strip('"')
            parts = text.split("~")
            if len(parts) < 32:
                raise ValueError("Unexpected Tencent response format")
            return Ticker(
                symbol=symbol,
                last_price=float(parts[3]),
                bid=float(parts[9]),
                ask=float(parts[19]),
                volume_24h=float(parts[36]) if len(parts) > 36 else 0.0,
                change_24h_pct=float(parts[32]) if len(parts) > 32 else 0.0,
                timestamp=parts[30] if len(parts) > 30 else "",
            )
        except Exception as exc:
            logger.error("Tencent ticker error for %s: %s", symbol, exc)
            return Ticker(symbol=symbol, last_price=0, bid=0, ask=0,
                          volume_24h=0, change_24h_pct=0, timestamp="")

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        return OrderBook(symbol=symbol)

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        return [{"symbol": query, "name": query, "exchange": "Tencent"}]
