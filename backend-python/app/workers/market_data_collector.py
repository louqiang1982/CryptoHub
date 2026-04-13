"""Market data collector worker.

Periodically fetches and caches OHLCV, ticker, and order-book data for
watched symbols.
"""

from __future__ import annotations

import logging
from typing import Any

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

# Default list of symbols to track
DEFAULT_SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "SOL/USDT",
    "XRP/USDT",
]


@celery_app.task(name="app.workers.market_data_collector.collect_market_data")
def collect_market_data() -> dict[str, Any]:
    """Fetch and cache latest market data for default symbols."""

    logger.info("Collecting market data …")
    collected: list[str] = []
    errors: list[str] = []

    # TODO: Instantiate CryptoDataProvider, fetch tickers/OHLCV,
    #       store results in Redis for fast access by the API layer.

    for symbol in DEFAULT_SYMBOLS:
        try:
            # Placeholder – replace with actual provider calls
            logger.debug("Collecting %s", symbol)
            collected.append(symbol)
        except Exception as exc:
            logger.error("Failed to collect %s: %s", symbol, exc)
            errors.append(symbol)

    return {
        "collected": collected,
        "errors": errors,
    }


@celery_app.task(name="app.workers.market_data_collector.collect_ohlcv")
def collect_ohlcv(symbol: str, timeframe: str = "1D", limit: int = 200) -> dict[str, Any]:
    """Fetch and cache OHLCV data for a single symbol."""

    logger.info("Collecting OHLCV for %s (%s)", symbol, timeframe)

    # TODO: Use CryptoDataProvider to fetch and cache in Redis

    return {"symbol": symbol, "timeframe": timeframe, "bars_fetched": 0}
