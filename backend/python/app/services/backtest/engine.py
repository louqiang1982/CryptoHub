"""Core backtest engine – simulates strategy execution on historical data."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any


from app.services.backtest.metrics import PerformanceMetrics, calculate_all
from app.services.strategy.script_strategy import Bar

logger = logging.getLogger(__name__)


@dataclass
class Trade:
    """Record of a single trade."""

    entry_time: str
    exit_time: str
    side: str
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    pnl_pct: float
    fees: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "side": self.side,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "quantity": self.quantity,
            "pnl": self.pnl,
            "pnl_pct": self.pnl_pct,
            "fees": self.fees,
        }


@dataclass
class BacktestConfig:
    """Configuration for a backtest run."""

    initial_capital: float = 10_000.0
    commission_pct: float = 0.1  # 0.1 % per trade
    slippage_pct: float = 0.05  # 0.05 % slippage
    position_size_pct: float = 100.0  # use 100% of capital per trade


@dataclass
class BacktestResult:
    """Full result set returned after a backtest run."""

    id: str = ""
    strategy_id: str = ""
    symbol: str = ""
    timeframe: str = ""
    start_date: str = ""
    end_date: str = ""
    config: BacktestConfig = field(default_factory=BacktestConfig)
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)
    metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    status: str = "completed"
    error_message: str | None = None

    @property
    def summary(self) -> dict[str, Any]:
        return {
            "total_return_pct": self.metrics.total_return_pct,
            "sharpe_ratio": self.metrics.sharpe_ratio,
            "sortino_ratio": self.metrics.sortino_ratio,
            "max_drawdown_pct": self.metrics.max_drawdown_pct,
            "win_rate": self.metrics.win_rate,
            "profit_factor": self.metrics.profit_factor,
            "total_trades": self.metrics.total_trades,
        }


class BacktestEngine:
    """Run a strategy against historical bar data and produce performance metrics."""

    def __init__(self, config: BacktestConfig | None = None) -> None:
        self.config = config or BacktestConfig()

    def run(
        self,
        bars: list[Bar],
        strategy_signals: list[dict[str, Any]],
        *,
        symbol: str = "",
        strategy_id: str = "",
        timeframe: str = "1D",
    ) -> BacktestResult:
        """Execute the backtest loop.

        Parameters
        ----------
        bars:
            Historical OHLCV bars.
        strategy_signals:
            List of dicts with keys ``index`` (bar index), ``action``
            (``"buy"`` / ``"sell"``), and optionally ``quantity``.
        """
        capital = self.config.initial_capital
        position: float = 0.0
        entry_price: float = 0.0
        entry_time: str = ""
        trades: list[Trade] = []
        equity_curve: list[float] = [capital]

        signal_map: dict[int, dict] = {s["index"]: s for s in strategy_signals}

        for idx, bar in enumerate(bars):
            signal = signal_map.get(idx)
            if signal is not None:
                action = signal.get("action", "").lower()
                if action == "buy" and position == 0.0:
                    qty = signal.get("quantity", self._default_quantity(capital, bar.close))
                    cost = qty * bar.close
                    fee = cost * self.config.commission_pct / 100.0
                    slip = cost * self.config.slippage_pct / 100.0
                    if cost + fee + slip <= capital:
                        capital -= cost + fee + slip
                        position = qty
                        entry_price = bar.close
                        entry_time = bar.timestamp

                elif action == "sell" and position > 0.0:
                    proceeds = position * bar.close
                    fee = proceeds * self.config.commission_pct / 100.0
                    slip = proceeds * self.config.slippage_pct / 100.0
                    net = proceeds - fee - slip
                    pnl = net - (position * entry_price)
                    pnl_pct = pnl / (position * entry_price) * 100.0 if entry_price else 0.0
                    trades.append(
                        Trade(
                            entry_time=entry_time,
                            exit_time=bar.timestamp,
                            side="long",
                            entry_price=entry_price,
                            exit_price=bar.close,
                            quantity=position,
                            pnl=pnl,
                            pnl_pct=pnl_pct,
                            fees=fee + slip,
                        )
                    )
                    capital += net
                    position = 0.0

            # Mark-to-market equity
            equity = capital + position * bar.close
            equity_curve.append(equity)

        trade_dicts = [t.to_dict() for t in trades]
        metrics = calculate_all(equity_curve, trade_dicts, self.config.initial_capital)

        return BacktestResult(
            strategy_id=strategy_id,
            symbol=symbol,
            timeframe=timeframe,
            start_date=bars[0].timestamp if bars else "",
            end_date=bars[-1].timestamp if bars else "",
            config=self.config,
            trades=trades,
            equity_curve=equity_curve,
            metrics=metrics,
        )

    # ------------------------------------------------------------------
    def _default_quantity(self, capital: float, price: float) -> float:
        """Determine default position size based on config."""
        if price <= 0:
            return 0.0
        available = capital * self.config.position_size_pct / 100.0
        return available / price
