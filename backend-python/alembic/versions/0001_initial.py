"""create initial tables

Revision ID: 0001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- strategies ---
    op.create_table(
        "strategies",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("strategy_type", sa.String(50), server_default="indicator"),
        sa.Column("code", sa.Text, nullable=True),
        sa.Column("symbol", sa.String(50), nullable=False),
        sa.Column("timeframe", sa.String(10), server_default="1H"),
        sa.Column("exchange", sa.String(50), server_default="binance"),
        sa.Column("status", sa.String(20), server_default="stopped"),
        sa.Column("is_live", sa.Boolean, server_default="false"),
        sa.Column("parameters", sa.JSON, nullable=True),
        sa.Column("max_position_size", sa.Float, server_default="1.0"),
        sa.Column("stop_loss_pct", sa.Float, nullable=True),
        sa.Column("take_profit_pct", sa.Float, nullable=True),
        sa.Column("total_trades", sa.Integer, server_default="0"),
        sa.Column("win_rate", sa.Float, server_default="0.0"),
        sa.Column("total_pnl", sa.Float, server_default="0.0"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # --- backtest_results ---
    op.create_table(
        "backtest_results",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("strategy_id", sa.String(36), nullable=False, index=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("symbol", sa.String(50), nullable=False),
        sa.Column("timeframe", sa.String(10), nullable=False),
        sa.Column("start_date", sa.String(20), nullable=False),
        sa.Column("end_date", sa.String(20), nullable=False),
        sa.Column("initial_capital", sa.Float, server_default="10000.0"),
        sa.Column("final_capital", sa.Float, server_default="0.0"),
        sa.Column("total_return_pct", sa.Float, server_default="0.0"),
        sa.Column("sharpe_ratio", sa.Float, server_default="0.0"),
        sa.Column("sortino_ratio", sa.Float, server_default="0.0"),
        sa.Column("max_drawdown_pct", sa.Float, server_default="0.0"),
        sa.Column("win_rate", sa.Float, server_default="0.0"),
        sa.Column("profit_factor", sa.Float, server_default="0.0"),
        sa.Column("total_trades", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("trades", sa.JSON, nullable=True),
        sa.Column("equity_curve", sa.JSON, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # --- indicators ---
    op.create_table(
        "indicators",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("author_id", sa.String(36), nullable=False, index=True),
        sa.Column("code", sa.Text, nullable=False),
        sa.Column("category", sa.String(50), server_default="custom"),
        sa.Column("is_public", sa.Boolean, server_default="false"),
        sa.Column("is_premium", sa.Boolean, server_default="false"),
        sa.Column("price", sa.Float, server_default="0.0"),
        sa.Column("parameters", sa.JSON, nullable=True),
        sa.Column("downloads", sa.Integer, server_default="0"),
        sa.Column("rating", sa.Float, server_default="0.0"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # --- ai_analyses ---
    op.create_table(
        "ai_analyses",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False, index=True),
        sa.Column("symbol", sa.String(50), nullable=False),
        sa.Column("analysis_type", sa.String(50), server_default="comprehensive"),
        sa.Column("signal", sa.String(10), server_default="hold"),
        sa.Column("confidence", sa.Float, server_default="0.0"),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("technical_analysis", sa.JSON, nullable=True),
        sa.Column("fundamental_analysis", sa.JSON, nullable=True),
        sa.Column("sentiment_analysis", sa.JSON, nullable=True),
        sa.Column("recommendation", sa.Text, nullable=True),
        sa.Column("llm_provider", sa.String(50), server_default="openai"),
        sa.Column("llm_model", sa.String(100), server_default="gpt-4o"),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ai_analyses")
    op.drop_table("indicators")
    op.drop_table("backtest_results")
    op.drop_table("strategies")
