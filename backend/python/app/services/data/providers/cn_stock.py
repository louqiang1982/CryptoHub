"""China A-share data provider using AKShare (free mainland China data)."""

from __future__ import annotations

import logging
from typing import Any

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook

logger = logging.getLogger(__name__)

try:
    import akshare as ak  # type: ignore[import]
    AKSHARE_AVAILABLE = True
except ImportError:
    ak = None  # type: ignore[assignment]
    AKSHARE_AVAILABLE = False
    logger.warning("akshare not installed – CnStockDataProvider returns empty data")


class CnStockDataProvider(BaseDataProvider):
    """A-share (Shanghai/Shenzhen) data provider backed by AKShare."""

    name = "cn_stock"

    async def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1D",
        limit: int = 100,
    ) -> list[OHLCV]:
        if not AKSHARE_AVAILABLE:
            return []
        try:
            import asyncio
            df = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: ak.stock_zh_a_hist(
                    symbol=symbol, period="daily", adjust="qfq"
                ).tail(limit),
            )
            return [
                OHLCV(
                    timestamp=str(row["日期"]),
                    open=float(row["开盘"]),
                    high=float(row["最高"]),
                    low=float(row["最低"]),
                    close=float(row["收盘"]),
                    volume=float(row["成交量"]),
                )
                for _, row in df.iterrows()
            ]
        except Exception as exc:
            logger.error("CnStock OHLCV error for %s: %s", symbol, exc)
            return []

    async def get_ticker(self, symbol: str) -> Ticker:
        if not AKSHARE_AVAILABLE:
            return Ticker(symbol=symbol, last_price=0, bid=0, ask=0,
                          volume_24h=0, change_24h_pct=0, timestamp="")
        try:
            import asyncio
            df = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ak.stock_zh_a_spot_em()
            )
            row = df[df["代码"] == symbol]
            if row.empty:
                raise ValueError(f"Symbol {symbol} not found")
            r = row.iloc[0]
            return Ticker(
                symbol=symbol,
                last_price=float(r.get("最新价", 0)),
                bid=float(r.get("买一", 0)),
                ask=float(r.get("卖一", 0)),
                volume_24h=float(r.get("成交量", 0)),
                change_24h_pct=float(r.get("涨跌幅", 0)),
                timestamp="",
            )
        except Exception as exc:
            logger.error("CnStock ticker error for %s: %s", symbol, exc)
            return Ticker(symbol=symbol, last_price=0, bid=0, ask=0,
                          volume_24h=0, change_24h_pct=0, timestamp="")

    async def get_order_book(self, symbol: str, depth: int = 20) -> OrderBook:
        return OrderBook(symbol=symbol)

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        if not AKSHARE_AVAILABLE:
            return []
        try:
            import asyncio
            df = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ak.stock_zh_a_spot_em()
            )
            mask = df["名称"].str.contains(query, na=False) | df["代码"].str.contains(query, na=False)
            return [
                {"symbol": r["代码"], "name": r["名称"], "exchange": "A-Share"}
                for _, r in df[mask].head(20).iterrows()
            ]
        except Exception as exc:
            logger.error("CnStock search error: %s", exc)
            return []
