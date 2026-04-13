"""Celery application factory."""

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "cryptohub",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "collect-market-data": {
            "task": "app.workers.market_data_collector.collect_market_data",
            "schedule": 60.0,  # every 60 seconds
        },
        "monitor-portfolios": {
            "task": "app.workers.portfolio_monitor.monitor_portfolios",
            "schedule": 300.0,  # every 5 minutes
        },
        "refresh-polymarket": {
            "task": "app.workers.polymarket_worker.refresh_polymarket_data",
            "schedule": 600.0,  # every 10 minutes
        },
    },
)

# Auto-discover task modules
celery_app.autodiscover_tasks(
    [
        "app.workers.pending_orders",
        "app.workers.portfolio_monitor",
        "app.workers.market_data_collector",
        "app.workers.reflection_worker",
        "app.workers.polymarket_worker",
    ]
)
