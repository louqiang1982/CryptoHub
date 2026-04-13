"""Tests for strategy-related services."""

import pytest

from app.services.strategy.compiler import StrategyCompiler
from app.services.strategy.runtime import StrategyRuntime, StrategyState
from app.services.strategy.script_strategy import ScriptStrategy, Bar, Order
from app.services.strategy.indicator_strategy import IndicatorStrategy
from app.services.strategy.snapshot import StrategySnapshot


class TestStrategyCompiler:
    def test_valid_code(self):
        code = """
def on_init():
    pass

def on_bar(bar):
    pass
"""
        compiler = StrategyCompiler()
        result = compiler.compile(code)
        assert result.success is True
        assert result.errors == []

    def test_syntax_error(self):
        code = "def broken(:"
        compiler = StrategyCompiler()
        result = compiler.compile(code)
        assert result.success is False
        assert len(result.errors) > 0

    def test_forbidden_import(self):
        code = "import os\ndef on_init(): pass\ndef on_bar(bar): pass"
        compiler = StrategyCompiler()
        result = compiler.compile(code)
        assert result.success is False

    def test_missing_methods_warning(self):
        code = "x = 1"
        compiler = StrategyCompiler()
        result = compiler.compile(code)
        assert len(result.warnings) > 0


class TestStrategyRuntime:
    @pytest.mark.asyncio
    async def test_start_and_stop(self):
        runtime = StrategyRuntime()
        assert await runtime.start("s1") is True
        assert runtime.get_state("s1") == StrategyState.RUNNING
        assert await runtime.stop("s1") is True
        assert runtime.get_state("s1") == StrategyState.STOPPED

    @pytest.mark.asyncio
    async def test_double_start(self):
        runtime = StrategyRuntime()
        await runtime.start("s1")
        assert await runtime.start("s1") is False

    @pytest.mark.asyncio
    async def test_list_running(self):
        runtime = StrategyRuntime()
        await runtime.start("a")
        await runtime.start("b")
        assert set(runtime.list_running()) == {"a", "b"}


class TestIndicatorStrategy:
    def test_buy_signal(self):
        strategy = IndicatorStrategy(name="SMA", symbol="BTC", parameters={"sma_period": 3})
        data = {"close": [100, 102, 104, 106, 108]}
        signals = strategy.evaluate(data)
        assert len(signals) > 0
        assert signals[0].action in ("buy", "sell")

    def test_insufficient_data(self):
        strategy = IndicatorStrategy(name="SMA", symbol="BTC", parameters={"sma_period": 20})
        data = {"close": [100]}
        signals = strategy.evaluate(data)
        assert signals == []


class TestStrategySnapshot:
    def test_capture_and_restore(self):
        snap = StrategySnapshot("test-1")
        state = snap.capture(position=1.5, orders=[{"id": "o1"}], variables={"x": 42})
        assert state["position"] == 1.5

        serialized = snap.serialize()
        restored = StrategySnapshot.deserialize(serialized)
        data = restored.restore()
        assert data["position"] == 1.5
        assert data["variables"]["x"] == 42
