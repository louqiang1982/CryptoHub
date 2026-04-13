"""Indicator SQLAlchemy models."""

from sqlalchemy import String, Text, Float, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Indicator(BaseModel):
    __tablename__ = "indicators"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="custom")
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    downloads: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
