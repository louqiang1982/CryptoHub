"""Shared test fixtures and configuration."""

import pytest


@pytest.fixture
def sample_bars():
    """Provide sample OHLCV bars for testing."""
    from app.services.strategy.script_strategy import Bar

    return [
        Bar(timestamp=f"2024-01-{str(d).zfill(2)}", open=100 + d, high=105 + d, low=98 + d, close=102 + d, volume=1000)
        for d in range(1, 31)
    ]


@pytest.fixture
def sample_trades():
    """Provide sample trade dicts for metric testing."""
    return [
        {"entry_time": "2024-01-01", "exit_time": "2024-01-05", "pnl": 150.0},
        {"entry_time": "2024-01-06", "exit_time": "2024-01-10", "pnl": -50.0},
        {"entry_time": "2024-01-11", "exit_time": "2024-01-15", "pnl": 200.0},
        {"entry_time": "2024-01-16", "exit_time": "2024-01-20", "pnl": -30.0},
        {"entry_time": "2024-01-21", "exit_time": "2024-01-25", "pnl": 80.0},
    ]


@pytest.fixture
def sample_equity_curve():
    """Provide a sample equity curve."""
    return [10000, 10150, 10100, 10300, 10270, 10350, 10200, 10400, 10500, 10450]
