"""Experiment scoring — evaluate and rank strategy/AI experiment results."""

from __future__ import annotations

import logging
import statistics
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExperimentScore:
    experiment_id: str
    total_score: float
    return_score: float
    risk_score: float
    consistency_score: float
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "total_score": round(self.total_score, 4),
            "return_score": round(self.return_score, 4),
            "risk_score": round(self.risk_score, 4),
            "consistency_score": round(self.consistency_score, 4),
            "details": self.details,
        }


class ExperimentScorer:
    """Score an experiment result using a weighted composite metric.

    Weights
    -------
    return_weight:
        Weight for total-return component (default 0.4).
    risk_weight:
        Weight for risk-adjusted return (Sharpe-like) component (default 0.4).
    consistency_weight:
        Weight for consistency (low volatility of returns) component (default 0.2).
    """

    def __init__(
        self,
        return_weight: float = 0.4,
        risk_weight: float = 0.4,
        consistency_weight: float = 0.2,
    ) -> None:
        self._rw = return_weight
        self._rkw = risk_weight
        self._cw = consistency_weight

    def score(
        self,
        experiment_id: str,
        equity_curve: list[float],
        trades: list[dict[str, Any]] | None = None,
    ) -> ExperimentScore:
        """Compute a composite score from an equity curve and trade list."""
        if len(equity_curve) < 2:
            return ExperimentScore(
                experiment_id=experiment_id,
                total_score=0.0,
                return_score=0.0,
                risk_score=0.0,
                consistency_score=0.0,
                details={"error": "insufficient data"},
            )

        initial = equity_curve[0]
        final = equity_curve[-1]
        total_return = (final - initial) / initial if initial else 0.0

        # Period returns
        period_returns = [
            (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
            for i in range(1, len(equity_curve))
            if equity_curve[i - 1] != 0
        ]

        if len(period_returns) >= 2:
            std_dev = statistics.stdev(period_returns)
            mean_return = statistics.mean(period_returns)
            sharpe = mean_return / std_dev if std_dev > 0 else 0.0
        else:
            sharpe = 0.0
            std_dev = 0.0

        # Max drawdown
        peak = equity_curve[0]
        max_dd = 0.0
        for v in equity_curve:
            if v > peak:
                peak = v
            dd = (peak - v) / peak if peak else 0.0
            max_dd = max(max_dd, dd)

        # Component scores (normalised 0–1)
        return_score = max(0.0, min(1.0, (total_return + 1) / 2))
        risk_score = max(0.0, min(1.0, (sharpe + 3) / 6))
        consistency_score = max(0.0, 1.0 - max_dd)

        total = (
            self._rw * return_score
            + self._rkw * risk_score
            + self._cw * consistency_score
        )

        return ExperimentScore(
            experiment_id=experiment_id,
            total_score=total,
            return_score=return_score,
            risk_score=risk_score,
            consistency_score=consistency_score,
            details={
                "total_return_pct": round(total_return * 100, 2),
                "sharpe_ratio": round(sharpe, 4),
                "max_drawdown_pct": round(max_dd * 100, 2),
                "return_std": round(std_dev * 100, 4),
                "num_periods": len(equity_curve),
                "num_trades": len(trades) if trades else 0,
            },
        )

    def rank(self, scores: list[ExperimentScore]) -> list[ExperimentScore]:
        """Return scores sorted by total_score descending."""
        return sorted(scores, key=lambda s: s.total_score, reverse=True)
