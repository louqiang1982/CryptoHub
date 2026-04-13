"""China & Hong Kong fundamentals data provider.

Fetches fundamental data such as P/E ratio, EPS, revenue, dividend yield
and analyst estimates for A-share and HK-listed companies.  Uses AKShare
for mainland data and Yahoo Finance for HK data.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class FundamentalsSnapshot:
    symbol: str
    name: str
    market_cap: float
    pe_ratio: float
    pb_ratio: float
    eps: float
    revenue: float
    dividend_yield: float
    roe: float
    debt_to_equity: float
    currency: str = "CNY"

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market_cap": self.market_cap,
            "pe_ratio": self.pe_ratio,
            "pb_ratio": self.pb_ratio,
            "eps": self.eps,
            "revenue": self.revenue,
            "dividend_yield": self.dividend_yield,
            "roe": self.roe,
            "debt_to_equity": self.debt_to_equity,
            "currency": self.currency,
        }


class CnHkFundamentalsProvider:
    """Fundamental data for A-share and HK-listed companies."""

    async def get_cn_stock_fundamentals(
        self, symbol: str
    ) -> FundamentalsSnapshot | None:
        """Fetch fundamentals for an A-share stock."""
        try:
            import asyncio

            try:
                import akshare as ak

                df = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ak.stock_a_lg_indicator(symbol=symbol)
                )
                if not df.empty:
                    latest = df.iloc[-1]
                    return FundamentalsSnapshot(
                        symbol=symbol,
                        name="",
                        market_cap=0.0,
                        pe_ratio=float(latest.get("pe", 0) or 0),
                        pb_ratio=float(latest.get("pb", 0) or 0),
                        eps=float(latest.get("eps", 0) or 0),
                        revenue=0.0,
                        dividend_yield=0.0,
                        roe=float(latest.get("roe", 0) or 0),
                        debt_to_equity=0.0,
                        currency="CNY",
                    )
            except ImportError:
                pass

            # Fallback: Yahoo Finance
            import yfinance as yf

            yf_sym = symbol if "." in symbol else f"{symbol}.SS"
            info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: yf.Ticker(yf_sym).info
            )
            return FundamentalsSnapshot(
                symbol=symbol,
                name=info.get("longName", ""),
                market_cap=float(info.get("marketCap", 0) or 0),
                pe_ratio=float(info.get("trailingPE", 0) or 0),
                pb_ratio=float(info.get("priceToBook", 0) or 0),
                eps=float(info.get("trailingEps", 0) or 0),
                revenue=float(info.get("totalRevenue", 0) or 0),
                dividend_yield=float(info.get("dividendYield", 0) or 0) * 100,
                roe=float(info.get("returnOnEquity", 0) or 0) * 100,
                debt_to_equity=float(info.get("debtToEquity", 0) or 0),
                currency=info.get("currency", "CNY"),
            )
        except Exception as exc:
            logger.error("CN fundamentals error for %s: %s", symbol, exc)
            return None

    async def get_hk_stock_fundamentals(
        self, symbol: str
    ) -> FundamentalsSnapshot | None:
        """Fetch fundamentals for an HK-listed stock."""
        try:
            import asyncio
            import yfinance as yf

            yf_sym = symbol if symbol.endswith(".HK") else f"{symbol}.HK"
            info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: yf.Ticker(yf_sym).info
            )
            return FundamentalsSnapshot(
                symbol=symbol,
                name=info.get("longName", ""),
                market_cap=float(info.get("marketCap", 0) or 0),
                pe_ratio=float(info.get("trailingPE", 0) or 0),
                pb_ratio=float(info.get("priceToBook", 0) or 0),
                eps=float(info.get("trailingEps", 0) or 0),
                revenue=float(info.get("totalRevenue", 0) or 0),
                dividend_yield=float(info.get("dividendYield", 0) or 0) * 100,
                roe=float(info.get("returnOnEquity", 0) or 0) * 100,
                debt_to_equity=float(info.get("debtToEquity", 0) or 0),
                currency="HKD",
            )
        except Exception as exc:
            logger.error("HK fundamentals error for %s: %s", symbol, exc)
            return None

    async def get_multiple(
        self, symbols: list[str], market: str = "cn"
    ) -> list[FundamentalsSnapshot]:
        """Batch fetch fundamentals."""
        results: list[FundamentalsSnapshot] = []
        for sym in symbols:
            snap = (
                await self.get_cn_stock_fundamentals(sym)
                if market == "cn"
                else await self.get_hk_stock_fundamentals(sym)
            )
            if snap:
                results.append(snap)
        return results
