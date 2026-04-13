"""DataFrame-based indicator strategy execution."""

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Signal:
    action: str  # "buy", "sell", "hold"
    symbol: str
    price: float
    quantity: float = 0.0
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class IndicatorStrategy:
    """Execute indicator-based trading strategies on DataFrames."""

    def __init__(self, name: str, symbol: str, parameters: dict | None = None):
        self.name = name
        self.symbol = symbol
        self.parameters = parameters or {}
        self.signals: list[Signal] = []

    def evaluate(self, data: dict[str, list[float]]) -> list[Signal]:
        self.signals = []
        closes = np.array(data.get("close", []))
        if len(closes) < 2:
            return self.signals

        sma_period = self.parameters.get("sma_period", 20)
        if len(closes) >= sma_period:
            sma = np.convolve(closes, np.ones(sma_period) / sma_period, mode="valid")
            current_price = closes[-1]
            current_sma = sma[-1]

            if current_price > current_sma:
                self.signals.append(Signal(
                    action="buy", symbol=self.symbol,
                    price=current_price, reason=f"Price above SMA({sma_period})"
                ))
            elif current_price < current_sma:
                self.signals.append(Signal(
                    action="sell", symbol=self.symbol,
                    price=current_price, reason=f"Price below SMA({sma_period})"
                ))
        return self.signals
