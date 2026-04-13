"""Portfolio monitoring worker.

Periodically evaluates portfolio health, checks risk limits, and fires
alerts when thresholds are breached.
"""

from __future__ import annotations

import logging
from typing import Any

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.portfolio_monitor.monitor_portfolios")
def monitor_portfolios() -> dict[str, Any]:
    """Evaluate all active portfolios against risk thresholds."""

    logger.info("Running portfolio monitoring sweep …")

    alerts: list[dict[str, Any]] = []

    # TODO: For each user portfolio
    # 1. Fetch current market prices
    # 2. Calculate unrealised PnL
    # 3. Check stop-loss / take-profit triggers
    # 4. Check max-drawdown thresholds
    # 5. Emit alerts / notifications as needed

    return {
        "portfolios_checked": 0,
        "alerts_generated": len(alerts),
        "alerts": alerts,
    }


@celery_app.task(name="app.workers.portfolio_monitor.rebalance_check")
def rebalance_check(user_id: str) -> dict[str, Any]:
    """Check whether a user's portfolio needs rebalancing."""

    logger.info("Rebalance check for user %s", user_id)

    # TODO: compare current allocation vs target allocation

    return {"user_id": user_id, "rebalance_needed": False, "drift_pct": 0.0}
