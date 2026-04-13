"""AI reflection worker.

Runs AI analysis reflection loops asynchronously to improve analysis
quality without blocking the API request.
"""

from __future__ import annotations

import logging
from typing import Any

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.reflection_worker.run_reflection")
def run_reflection(analysis_id: str, symbol: str, original_analysis: str) -> dict[str, Any]:
    """Execute a reflection loop on a completed analysis.

    This uses the :class:`ReflectionService` to critique, improve, and
    score the original analysis produced by the streaming LLM call.
    """

    logger.info("Running reflection for analysis %s on %s", analysis_id, symbol)

    # TODO: instantiate ReflectionService, call reflect_on_analysis,
    #       persist improved analysis back to the database.

    return {
        "analysis_id": analysis_id,
        "symbol": symbol,
        "status": "reflected",
        "improvement_score": 0.0,
    }


@celery_app.task(name="app.workers.reflection_worker.batch_reflect")
def batch_reflect(analysis_ids: list[str]) -> dict[str, Any]:
    """Run reflection on a batch of analyses."""

    logger.info("Batch reflection for %d analyses", len(analysis_ids))
    results: list[dict[str, Any]] = []

    for aid in analysis_ids:
        try:
            result = run_reflection(aid, symbol="", original_analysis="")
            results.append(result)
        except Exception as exc:
            logger.error("Reflection failed for %s: %s", aid, exc)

    return {"total": len(analysis_ids), "reflected": len(results)}
