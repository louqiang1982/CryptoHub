"""Polymarket prediction-market data worker.

Periodically fetches prediction market data from Polymarket and caches
it for the frontend.
"""

from __future__ import annotations

import logging
from typing import Any

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.polymarket_worker.refresh_polymarket_data")
def refresh_polymarket_data() -> dict[str, Any]:
    """Fetch latest prediction markets from Polymarket API and cache."""

    logger.info("Refreshing Polymarket data …")

    # TODO: Call PolymarketService.get_markets(), cache results in Redis.

    return {"markets_fetched": 0, "status": "ok"}


@celery_app.task(name="app.workers.polymarket_worker.track_market")
def track_market(market_id: str) -> dict[str, Any]:
    """Follow a specific market and track odds changes over time."""

    logger.info("Tracking Polymarket market %s", market_id)

    # TODO: Fetch market details, store historical snapshots.

    return {"market_id": market_id, "tracked": True}
