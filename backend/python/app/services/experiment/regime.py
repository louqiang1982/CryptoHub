"""Market regime detection — classifies current market state.

Regimes: trending_up, trending_down, ranging, volatile, crisis.
Uses volatility (ATR ratio), trend (EMA slope) and momentum signals.
"""

from __future__ import annotations

import logging
import statistics
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class Regime(str, Enum):
    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    RANGING = "ranging"
    VOLATILE = "volatile"
    CRISIS = "crisis"


def _ema(prices: list[float], period: int) -> list[float]:
    """Calculate EMA for a list of prices."""
    if not prices or period <= 0:
        return []
    k = 2 / (period + 1)
    ema: list[float] = [prices[0]]
    for p in prices[1:]:
        ema.append(p * k + ema[-1] * (1 - k))
    return ema


def _atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float:
    """Calculate average true range."""
    if len(highs) < 2:
        return 0.0
    trs: list[float] = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    return statistics.mean(trs[-period:]) if trs else 0.0


class RegimeDetector:
    """Detect the current market regime from OHLCV bars.

    Parameters
    ----------
    trend_period:
        EMA period for trend calculation.
    volatility_threshold:
        ATR/price ratio above which the market is considered volatile.
    crisis_threshold:
        Very high volatility that indicates a crisis regime.
    """

    def __init__(
        self,
        trend_period: int = 20,
        volatility_threshold: float = 0.02,
        crisis_threshold: float = 0.05,
    ) -> None:
        self._trend_period = trend_period
        self._vol_threshold = volatility_threshold
        self._crisis_threshold = crisis_threshold

    def detect(
        self,
        closes: list[float],
        highs: list[float] | None = None,
        lows: list[float] | None = None,
    ) -> dict[str, Any]:
        """Detect regime from price series.

        Returns a dict with 'regime', 'confidence', and supporting metrics.
        """
        if len(closes) < self._trend_period:
            return {"regime": Regime.RANGING, "confidence": 0.5, "metrics": {}}

        highs = highs or closes
        lows = lows or closes

        ema_vals = _ema(closes, self._trend_period)
        ema_slope = (ema_vals[-1] - ema_vals[-5]) / ema_vals[-5] if ema_vals[-5] != 0 else 0

        atr = _atr(highs, lows, closes)
        current_price = closes[-1]
        atr_ratio = atr / current_price if current_price != 0 else 0

        # Determine regime
        if atr_ratio >= self._crisis_threshold:
            regime = Regime.CRISIS
            confidence = min(1.0, atr_ratio / self._crisis_threshold)
        elif atr_ratio >= self._vol_threshold:
            regime = Regime.VOLATILE
            confidence = min(1.0, atr_ratio / self._vol_threshold)
        elif ema_slope > 0.005:
            regime = Regime.TRENDING_UP
            confidence = min(1.0, ema_slope / 0.02)
        elif ema_slope < -0.005:
            regime = Regime.TRENDING_DOWN
            confidence = min(1.0, abs(ema_slope) / 0.02)
        else:
            regime = Regime.RANGING
            confidence = 1.0 - abs(ema_slope) / 0.005

        return {
            "regime": regime,
            "confidence": round(max(0.0, min(1.0, confidence)), 3),
            "metrics": {
                "ema_slope": round(ema_slope, 6),
                "atr": round(atr, 6),
                "atr_ratio": round(atr_ratio, 6),
                "current_price": current_price,
            },
        }
