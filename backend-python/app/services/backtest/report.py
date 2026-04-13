"""Backtest report generation service."""

from __future__ import annotations

import logging
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

import numpy as np

from app.services.backtest.engine import BacktestResult

logger = logging.getLogger(__name__)


class BacktestReportService:
    """Generate human-readable and machine-readable backtest reports."""

    def generate(self, result: BacktestResult) -> dict[str, Any]:
        """Build a comprehensive report dict from a *BacktestResult*."""

        return {
            "overview": self._overview(result),
            "performance": asdict(result.metrics),
            "trades": [t.to_dict() for t in result.trades],
            "equity_curve": self._sampled_equity(result.equity_curve),
            "monthly_returns": self._monthly_returns(result),
            "drawdown_series": self._drawdown_series(result.equity_curve),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # ------------------------------------------------------------------
    @staticmethod
    def _overview(result: BacktestResult) -> dict[str, Any]:
        return {
            "symbol": result.symbol,
            "timeframe": result.timeframe,
            "start_date": result.start_date,
            "end_date": result.end_date,
            "initial_capital": result.config.initial_capital,
            "final_capital": result.equity_curve[-1] if result.equity_curve else 0.0,
            "total_trades": result.metrics.total_trades,
            "status": result.status,
        }

    @staticmethod
    def _sampled_equity(curve: list[float], max_points: int = 500) -> list[dict]:
        """Down-sample the equity curve to at most *max_points*."""
        if not curve:
            return []
        step = max(1, len(curve) // max_points)
        return [{"index": i, "equity": curve[i]} for i in range(0, len(curve), step)]

    @staticmethod
    def _drawdown_series(curve: list[float]) -> list[dict]:
        """Compute running drawdown percentage series."""
        if not curve:
            return []
        arr = np.asarray(curve, dtype=np.float64)
        peak = np.maximum.accumulate(arr)
        dd = np.where(peak > 0, (peak - arr) / peak * 100.0, 0.0)
        step = max(1, len(dd) // 500)
        return [{"index": i, "drawdown_pct": float(dd[i])} for i in range(0, len(dd), step)]

    @staticmethod
    def _monthly_returns(result: BacktestResult) -> list[dict]:
        """Aggregate trade PnL into monthly buckets (best-effort)."""
        monthly: dict[str, float] = {}
        for trade in result.trades:
            try:
                month_key = trade.exit_time[:7]  # "YYYY-MM"
            except (TypeError, IndexError):
                continue
            monthly[month_key] = monthly.get(month_key, 0.0) + trade.pnl
        return [{"month": k, "pnl": v} for k, v in sorted(monthly.items())]
