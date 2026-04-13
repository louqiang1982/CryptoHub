"""Backtest Pydantic schemas."""

from pydantic import BaseModel, Field


class BacktestRequest(BaseModel):
    strategy_id: str
    symbol: str
    timeframe: str = "1H"
    start_date: str
    end_date: str
    initial_capital: float = Field(default=10000.0, gt=0)


class BacktestResponse(BaseModel):
    id: str
    strategy_id: str
    symbol: str
    timeframe: str
    status: str
    initial_capital: float
    final_capital: float
    total_return_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown_pct: float
    win_rate: float
    profit_factor: float
    total_trades: int

    model_config = {"from_attributes": True}


class BacktestReport(BaseModel):
    backtest: BacktestResponse
    trades: list[dict] = []
    equity_curve: list[dict] = []
    monthly_returns: list[dict] = []
