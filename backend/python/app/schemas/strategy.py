"""Strategy Pydantic schemas."""

from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    strategy_type: str = "indicator"
    code: str | None = None
    symbol: str = Field(..., min_length=1)
    timeframe: str = "1H"
    exchange: str = "binance"
    parameters: dict | None = None
    max_position_size: float = 1.0
    stop_loss_pct: float | None = None
    take_profit_pct: float | None = None


class StrategyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    code: str | None = None
    parameters: dict | None = None
    max_position_size: float | None = None
    stop_loss_pct: float | None = None
    take_profit_pct: float | None = None


class StrategyResponse(BaseModel):
    id: str
    name: str
    description: str | None
    strategy_type: str
    symbol: str
    timeframe: str
    exchange: str
    status: str
    is_live: bool
    total_trades: int
    win_rate: float
    total_pnl: float

    model_config = {"from_attributes": True}


class StrategyRequest(BaseModel):
    """Request body for strategy compile/start endpoints."""

    code: str
    symbol: str = "BTC/USDT"
    parameters: dict | None = None
    strategy_type: str = "script"


class CompileRequest(BaseModel):
    code: str
    strategy_type: str = "script"


class CompileResponse(BaseModel):
    success: bool
    errors: list[str] = []
    warnings: list[str] = []
