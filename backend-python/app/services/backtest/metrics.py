"""Backtest performance metrics calculations."""

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class PerformanceMetrics:
    """Container for backtest performance metrics."""

    total_return_pct: float = 0.0
    annualized_return_pct: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    max_drawdown_pct: float = 0.0
    max_drawdown_duration_days: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_trade_pnl: float = 0.0
    calmar_ratio: float = 0.0
    volatility: float = 0.0


TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.04  # 4 % annual


def compute_returns(equity_curve: list[float]) -> np.ndarray:
    """Compute simple returns from an equity curve."""
    arr = np.asarray(equity_curve, dtype=np.float64)
    if len(arr) < 2:
        return np.array([], dtype=np.float64)
    return np.diff(arr) / arr[:-1]


def total_return(initial_capital: float, final_capital: float) -> float:
    """Compute total return percentage."""
    if initial_capital <= 0:
        return 0.0
    return (final_capital - initial_capital) / initial_capital * 100.0


def annualized_return(total_return_pct: float, trading_days: int) -> float:
    """Annualise a total return percentage."""
    if trading_days <= 0:
        return 0.0
    years = trading_days / TRADING_DAYS_PER_YEAR
    growth = 1.0 + total_return_pct / 100.0
    if growth <= 0:
        return -100.0
    return (growth ** (1.0 / years) - 1.0) * 100.0


def sharpe_ratio(
    returns: np.ndarray,
    risk_free_rate: float = RISK_FREE_RATE,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Compute annualised Sharpe ratio."""
    if len(returns) < 2:
        return 0.0
    daily_rf = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = returns - daily_rf
    std = np.std(excess, ddof=1)
    if std == 0:
        return 0.0
    return float(np.mean(excess) / std * math.sqrt(periods_per_year))


def sortino_ratio(
    returns: np.ndarray,
    risk_free_rate: float = RISK_FREE_RATE,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """Compute annualised Sortino ratio (downside-deviation denominator)."""
    if len(returns) < 2:
        return 0.0
    daily_rf = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = returns - daily_rf
    downside = excess[excess < 0]
    if len(downside) == 0:
        return 0.0
    downside_std = np.std(downside, ddof=1)
    if downside_std == 0:
        return 0.0
    return float(np.mean(excess) / downside_std * math.sqrt(periods_per_year))


def max_drawdown(equity_curve: list[float]) -> tuple[float, int]:
    """Return max drawdown percentage and its duration in bars.

    Returns
    -------
    (max_dd_pct, max_dd_duration)
    """
    if len(equity_curve) < 2:
        return 0.0, 0

    arr = np.asarray(equity_curve, dtype=np.float64)
    peak = arr[0]
    max_dd = 0.0
    dd_start = 0
    max_dd_dur = 0
    cur_dur = 0

    for i in range(1, len(arr)):
        if arr[i] > peak:
            peak = arr[i]
            dd_start = i
            cur_dur = 0
        else:
            dd = (peak - arr[i]) / peak * 100.0
            cur_dur = i - dd_start
            if dd > max_dd:
                max_dd = dd
                max_dd_dur = cur_dur

    return max_dd, max_dd_dur


def win_rate(trades: list[dict]) -> float:
    """Compute win rate from a list of trade dicts (each must have ``pnl``)."""
    if not trades:
        return 0.0
    winners = sum(1 for t in trades if t.get("pnl", 0) > 0)
    return winners / len(trades) * 100.0


def profit_factor(trades: list[dict]) -> float:
    """Compute profit factor = gross_profit / |gross_loss|."""
    gross_profit = sum(t["pnl"] for t in trades if t.get("pnl", 0) > 0)
    gross_loss = abs(sum(t["pnl"] for t in trades if t.get("pnl", 0) < 0))
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def calmar_ratio(annualized_ret: float, max_dd_pct: float) -> float:
    """Calmar ratio = annualized return / max drawdown."""
    if max_dd_pct == 0:
        return 0.0
    return annualized_ret / max_dd_pct


def calculate_all(
    equity_curve: list[float],
    trades: list[dict],
    initial_capital: float,
) -> PerformanceMetrics:
    """Compute all metrics in one call."""
    if not equity_curve:
        return PerformanceMetrics()

    final_capital = equity_curve[-1]
    ret = total_return(initial_capital, final_capital)
    ann_ret = annualized_return(ret, len(equity_curve))
    returns = compute_returns(equity_curve)
    dd, dd_dur = max_drawdown(equity_curve)
    sr = sharpe_ratio(returns)
    so = sortino_ratio(returns)
    wr = win_rate(trades)
    pf = profit_factor(trades)
    cr = calmar_ratio(ann_ret, dd)

    winners = [t for t in trades if t.get("pnl", 0) > 0]
    losers = [t for t in trades if t.get("pnl", 0) < 0]
    avg_w = float(np.mean([t["pnl"] for t in winners])) if winners else 0.0
    avg_l = float(np.mean([t["pnl"] for t in losers])) if losers else 0.0
    avg_pnl = float(np.mean([t.get("pnl", 0) for t in trades])) if trades else 0.0

    vol = float(np.std(returns, ddof=1) * math.sqrt(TRADING_DAYS_PER_YEAR) * 100.0) if len(returns) > 1 else 0.0

    return PerformanceMetrics(
        total_return_pct=ret,
        annualized_return_pct=ann_ret,
        sharpe_ratio=sr,
        sortino_ratio=so,
        max_drawdown_pct=dd,
        max_drawdown_duration_days=dd_dur,
        win_rate=wr,
        profit_factor=pf,
        total_trades=len(trades),
        winning_trades=len(winners),
        losing_trades=len(losers),
        avg_win=avg_w,
        avg_loss=avg_l,
        avg_trade_pnl=avg_pnl,
        calmar_ratio=cr,
        volatility=vol,
    )
