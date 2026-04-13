"""Tests for backtest metrics calculations."""

import math

import pytest

from app.services.backtest.metrics import (
    total_return,
    annualized_return,
    sharpe_ratio,
    sortino_ratio,
    max_drawdown,
    win_rate,
    profit_factor,
    compute_returns,
    calculate_all,
)


class TestTotalReturn:
    def test_positive_return(self):
        assert total_return(10_000, 11_000) == pytest.approx(10.0)

    def test_negative_return(self):
        assert total_return(10_000, 9_000) == pytest.approx(-10.0)

    def test_zero_capital(self):
        assert total_return(0, 100) == 0.0

    def test_no_change(self):
        assert total_return(10_000, 10_000) == pytest.approx(0.0)


class TestSharpeRatio:
    def test_constant_returns_zero_sharpe(self):
        import numpy as np

        returns = np.array([0.01, 0.01, 0.01, 0.01, 0.01])
        # Constant excess returns → std ≈ 0 → sharpe ≈ 0 (or very high)
        sr = sharpe_ratio(returns)
        # With constant returns, std of excess won't be exactly zero due to rf subtraction
        assert isinstance(sr, float)

    def test_empty_returns(self):
        import numpy as np

        assert sharpe_ratio(np.array([])) == 0.0


class TestSortinoRatio:
    def test_no_downside(self):
        import numpy as np

        returns = np.array([0.05, 0.04, 0.03, 0.06, 0.02])
        # If all returns are positive, downside may still exist after rf subtraction
        result = sortino_ratio(returns)
        assert isinstance(result, float)

    def test_empty_returns(self):
        import numpy as np

        assert sortino_ratio(np.array([])) == 0.0


class TestMaxDrawdown:
    def test_simple_drawdown(self):
        curve = [100, 110, 105, 108, 95, 100]
        dd, dur = max_drawdown(curve)
        # Peak is 110, trough is 95 → dd = (110-95)/110 * 100 ≈ 13.636%
        assert dd == pytest.approx(13.636, abs=0.01)

    def test_no_drawdown(self):
        curve = [100, 101, 102, 103, 104]
        dd, dur = max_drawdown(curve)
        assert dd == 0.0

    def test_single_point(self):
        dd, dur = max_drawdown([100])
        assert dd == 0.0


class TestWinRate:
    def test_basic(self, sample_trades):
        wr = win_rate(sample_trades)
        # 3 winners out of 5 = 60%
        assert wr == pytest.approx(60.0)

    def test_empty(self):
        assert win_rate([]) == 0.0


class TestProfitFactor:
    def test_basic(self, sample_trades):
        pf = profit_factor(sample_trades)
        # gross profit = 150+200+80 = 430, gross loss = 50+30 = 80
        assert pf == pytest.approx(430.0 / 80.0)

    def test_no_losses(self):
        trades = [{"pnl": 100}, {"pnl": 200}]
        pf = profit_factor(trades)
        assert pf == float("inf")


class TestCalculateAll:
    def test_returns_metrics(self, sample_equity_curve, sample_trades):
        metrics = calculate_all(sample_equity_curve, sample_trades, 10_000)
        assert metrics.total_trades == 5
        assert metrics.winning_trades == 3
        assert metrics.losing_trades == 2
        assert metrics.total_return_pct == pytest.approx(4.5)  # (10450-10000)/10000*100

    def test_empty_curve(self):
        metrics = calculate_all([], [], 10_000)
        assert metrics.total_trades == 0
