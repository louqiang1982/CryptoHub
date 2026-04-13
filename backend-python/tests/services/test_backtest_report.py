"""Tests for the backtest report service."""

import pytest

from app.services.backtest.engine import BacktestEngine, BacktestConfig
from app.services.backtest.report import BacktestReportService
from app.services.strategy.script_strategy import Bar


class TestBacktestReportService:
    def _run_basic_backtest(self):
        bars = [
            Bar(timestamp=f"2024-01-{str(i + 1).zfill(2)}", open=100 + i, high=106 + i, low=98 + i, close=102 + i, volume=1000)
            for i in range(20)
        ]
        signals = [
            {"index": 0, "action": "buy"},
            {"index": 10, "action": "sell"},
            {"index": 12, "action": "buy"},
            {"index": 19, "action": "sell"},
        ]
        config = BacktestConfig(initial_capital=10_000, commission_pct=0, slippage_pct=0)
        engine = BacktestEngine(config)
        return engine.run(bars, signals)

    def test_report_structure(self):
        result = self._run_basic_backtest()
        service = BacktestReportService()
        report = service.generate(result)

        assert "overview" in report
        assert "performance" in report
        assert "trades" in report
        assert "equity_curve" in report
        assert "monthly_returns" in report
        assert "drawdown_series" in report
        assert "generated_at" in report

    def test_overview_fields(self):
        result = self._run_basic_backtest()
        service = BacktestReportService()
        report = service.generate(result)
        overview = report["overview"]

        assert "initial_capital" in overview
        assert "final_capital" in overview
        assert "total_trades" in overview
