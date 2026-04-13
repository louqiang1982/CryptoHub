"""Pending-order processing worker.

Checks for pending limit / stop orders and executes them when market
conditions are met.
"""

from __future__ import annotations

import logging
from typing import Any

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.pending_orders.process_pending_orders")
def process_pending_orders() -> dict[str, Any]:
    """Scan pending orders and execute those whose trigger conditions are met."""

    logger.info("Scanning pending orders …")
    executed: list[str] = []
    failed: list[str] = []

    # TODO: query DB for pending orders, check current market prices,
    #       execute matching orders via the exchange connector.

    return {
        "scanned": 0,
        "executed": executed,
        "failed": failed,
    }


@celery_app.task(name="app.workers.pending_orders.cancel_expired_orders")
def cancel_expired_orders() -> dict[str, Any]:
    """Cancel orders that have exceeded their time-to-live."""

    logger.info("Checking for expired orders …")
    cancelled: list[str] = []

    # TODO: query DB for orders past their expiry timestamp

    return {"cancelled": cancelled}
