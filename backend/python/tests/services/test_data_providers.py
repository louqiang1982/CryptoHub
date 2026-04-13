"""Tests for data provider base class and implementations."""

import pytest

from app.services.data.providers.base import BaseDataProvider, OHLCV, Ticker, OrderBook


class TestOHLCV:
    def test_creation(self):
        bar = OHLCV(timestamp="2024-01-01", open=100, high=105, low=98, close=102, volume=1000)
        assert bar.close == 102

    def test_fields(self):
        bar = OHLCV(timestamp="t", open=1, high=2, low=0.5, close=1.5, volume=100)
        assert bar.high > bar.low


class TestTicker:
    def test_creation(self):
        ticker = Ticker(
            symbol="BTC/USDT",
            last_price=50000,
            bid=49999,
            ask=50001,
            volume_24h=1e9,
            change_24h_pct=2.5,
            timestamp="2024-01-01T00:00:00Z",
        )
        assert ticker.symbol == "BTC/USDT"
        assert ticker.last_price == 50000


class TestBaseDataProvider:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            BaseDataProvider()  # type: ignore[abstract]
