"""Strategy SQLAlchemy models."""

from sqlalchemy import String, Text, Float, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Strategy(BaseModel):
    __tablename__ = "strategies"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy_type: Mapped[str] = mapped_column(String(50), default="indicator")
    code: Mapped[str | None] = mapped_column(Text, nullable=True)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(10), default="1H")
    exchange: Mapped[str] = mapped_column(String(50), default="binance")
    status: Mapped[str] = mapped_column(String(20), default="stopped")
    is_live: Mapped[bool] = mapped_column(Boolean, default=False)
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    max_position_size: Mapped[float] = mapped_column(Float, default=1.0)
    stop_loss_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    take_profit_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_trades: Mapped[int] = mapped_column(Integer, default=0)
    win_rate: Mapped[float] = mapped_column(Float, default=0.0)
    total_pnl: Mapped[float] = mapped_column(Float, default=0.0)
