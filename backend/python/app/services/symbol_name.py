"""Symbol name resolver — maps exchange-specific tickers to human-readable names.

Supports crypto, US stocks, A-shares, HK stocks, forex, futures, and
Polymarket market IDs.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# Well-known crypto symbols
_CRYPTO_NAMES: dict[str, str] = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "BNB": "BNB",
    "SOL": "Solana",
    "XRP": "XRP",
    "ADA": "Cardano",
    "DOGE": "Dogecoin",
    "AVAX": "Avalanche",
    "LINK": "Chainlink",
    "MATIC": "Polygon",
    "DOT": "Polkadot",
    "UNI": "Uniswap",
    "ATOM": "Cosmos",
    "LTC": "Litecoin",
    "BCH": "Bitcoin Cash",
    "TRX": "TRON",
    "NEAR": "NEAR Protocol",
    "APT": "Aptos",
    "OP": "Optimism",
    "ARB": "Arbitrum",
    "USDT": "Tether",
    "USDC": "USD Coin",
    "BUSD": "Binance USD",
}

_FOREX_NAMES: dict[str, str] = {
    "EURUSD": "Euro / US Dollar",
    "GBPUSD": "British Pound / US Dollar",
    "USDJPY": "US Dollar / Japanese Yen",
    "USDCHF": "US Dollar / Swiss Franc",
    "AUDUSD": "Australian Dollar / US Dollar",
    "USDCAD": "US Dollar / Canadian Dollar",
    "NZDUSD": "New Zealand Dollar / US Dollar",
    "EURGBP": "Euro / British Pound",
    "EURJPY": "Euro / Japanese Yen",
    "GBPJPY": "British Pound / Japanese Yen",
}

_FUTURES_NAMES: dict[str, str] = {
    "CL": "Crude Oil Futures",
    "GC": "Gold Futures",
    "SI": "Silver Futures",
    "NG": "Natural Gas Futures",
    "ZC": "Corn Futures",
    "ZW": "Wheat Futures",
    "ES": "E-mini S&P 500",
    "NQ": "E-mini Nasdaq 100",
    "YM": "E-mini Dow Jones",
    "RTY": "E-mini Russell 2000",
}


def _normalise(symbol: str) -> str:
    """Strip exchange prefix and case-normalise."""
    sym = symbol.upper().strip()
    # Strip CCXT-style "BTC/USDT:USDT" perpetual notation
    if "/" in sym:
        sym = sym.split("/")[0]
    # Strip exchange prefix like "BINANCE:BTC"
    if ":" in sym:
        sym = sym.split(":")[-1]
    return sym


class SymbolNameResolver:
    """Resolve a ticker symbol to a display name and asset class."""

    def resolve(self, symbol: str) -> dict[str, Any]:
        """Return display name and asset class for *symbol*."""
        sym = _normalise(symbol)

        # Crypto
        crypto_base = sym.replace("USDT", "").replace("BUSD", "").replace("USDC", "")
        if sym in _CRYPTO_NAMES:
            return {"symbol": symbol, "name": _CRYPTO_NAMES[sym], "asset_class": "crypto"}
        if crypto_base in _CRYPTO_NAMES:
            return {
                "symbol": symbol,
                "name": f"{_CRYPTO_NAMES[crypto_base]} / USDT",
                "asset_class": "crypto",
            }

        # Forex
        if sym in _FOREX_NAMES:
            return {"symbol": symbol, "name": _FOREX_NAMES[sym], "asset_class": "forex"}

        # Futures
        if sym.rstrip("=F").rstrip("F") in _FUTURES_NAMES:
            base = sym.rstrip("=F").rstrip("F")
            return {
                "symbol": symbol,
                "name": _FUTURES_NAMES.get(base, f"{base} Futures"),
                "asset_class": "futures",
            }

        # US stocks (simple heuristic: alphabetic, 1-5 chars)
        if sym.isalpha() and 1 <= len(sym) <= 5:
            return {"symbol": symbol, "name": sym, "asset_class": "us_stock"}

        # A-share (6-digit numeric code)
        if sym.isdigit() and len(sym) == 6:
            return {"symbol": symbol, "name": sym, "asset_class": "cn_stock"}

        # HK stock (4-5 digit numeric)
        if sym.isdigit() and 4 <= len(sym) <= 5:
            return {"symbol": symbol, "name": sym, "asset_class": "hk_stock"}

        return {"symbol": symbol, "name": symbol, "asset_class": "unknown"}

    def resolve_many(self, symbols: list[str]) -> list[dict[str, Any]]:
        return [self.resolve(s) for s in symbols]

    def infer_asset_class(self, symbol: str) -> str:
        return self.resolve(symbol).get("asset_class", "unknown")
