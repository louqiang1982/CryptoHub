"""Tests for the backtest engine."""

import pytest

from app.services.backtest.engine import BacktestEngine, BacktestConfig
from app.services.strategy.script_strategy import Bar


class TestBacktestEngine:
    def _make_bars(self, prices: list[float]) -> list[Bar]:
        return [
            Bar(timestamp=f"2024-01-{str(i + 1).zfill(2)}", open=p, high=p + 5, low=p - 5, close=p, volume=1000)
            for i, p in enumerate(prices)
        ]

    def test_buy_and_sell(self):
        bars = self._make_bars([100, 105, 110, 108, 115])
        signals = [
            {"index": 0, "action": "buy"},
            {"index": 4, "action": "sell"},
        ]
        config = BacktestConfig(initial_capital=10_000, commission_pct=0, slippage_pct=0)
        engine = BacktestEngine(config)
        result = engine.run(bars, signals, symbol="TEST")

        assert result.metrics.total_trades == 1
        assert result.trades[0].entry_price == 100
        assert result.trades[0].exit_price == 115
        assert result.metrics.total_return_pct > 0

    def test_no_signals(self):
        bars = self._make_bars([100, 105, 110])
        engine = BacktestEngine()
        result = engine.run(bars, [])
        assert result.metrics.total_trades == 0

    def test_equity_curve_length(self):
        bars = self._make_bars([100, 105, 110])
        engine = BacktestEngine()
        result = engine.run(bars, [])
        # initial + one per bar
        assert len(result.equity_curve) == len(bars) + 1
