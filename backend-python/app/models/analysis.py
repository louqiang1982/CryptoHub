"""AI Analysis SQLAlchemy models."""

from sqlalchemy import String, Text, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AIAnalysis(BaseModel):
    __tablename__ = "ai_analyses"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    analysis_type: Mapped[str] = mapped_column(String(50), default="comprehensive")
    signal: Mapped[str] = mapped_column(String(10), default="hold")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    technical_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    fundamental_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sentiment_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    llm_provider: Mapped[str] = mapped_column(String(50), default="openai")
    llm_model: Mapped[str] = mapped_column(String(100), default="gpt-4o")
    status: Mapped[str] = mapped_column(String(20), default="pending")
