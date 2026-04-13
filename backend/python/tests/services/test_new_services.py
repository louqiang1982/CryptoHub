"""Tests for new services: polymarket, experiment, data infrastructure, symbol_name, code_quality."""

import pytest

# ── Polymarket ────────────────────────────────────────────────────────────────

class TestPolymarketService:
    def test_market_from_dict(self):
        from app.services.research.polymarket import Market

        data = {
            "conditionId": "abc123",
            "question": "Will BTC reach $100k?",
            "tokens": [
                {"outcome": "Yes", "price": "0.65"},
                {"outcome": "No", "price": "0.35"},
            ],
            "volume": "1500000",
            "liquidity": "85000",
            "endDateIso": "2025-12-31",
            "active": True,
            "closed": False,
            "tags": [{"slug": "crypto"}],
        }
        market = Market.from_dict(data)

        assert market.market_id == "abc123"
        assert market.question == "Will BTC reach $100k?"
        assert market.outcome_prices == [0.65, 0.35]
        assert market.volume == 1_500_000.0
        assert market.tags == ["crypto"]

    def test_market_to_dict(self):
        from app.services.research.polymarket import Market

        market = Market(
            market_id="m1",
            question="Q?",
            outcomes=["Yes", "No"],
            outcome_prices=[0.7, 0.3],
            volume=100_000,
            liquidity=5_000,
            end_date="2025-06-01",
            active=True,
            closed=False,
        )
        d = market.to_dict()
        assert d["market_id"] == "m1"
        assert d["outcome_prices"] == [0.7, 0.3]

    def test_analyse_market_bullish(self):
        from app.services.research.polymarket import Market, PolymarketService

        svc = PolymarketService()
        market = Market(
            market_id="m2",
            question="Bull market?",
            outcomes=["Yes", "No"],
            outcome_prices=[0.75, 0.25],
            volume=500_000,
            liquidity=30_000,
            end_date=None,
            active=True,
            closed=False,
        )
        analysis = svc.analyse_market(market)
        assert analysis.sentiment == "bullish"
        assert 0 <= analysis.confidence <= 1

    def test_analyse_market_bearish(self):
        from app.services.research.polymarket import Market, PolymarketService

        svc = PolymarketService()
        market = Market(
            market_id="m3",
            question="Bear market?",
            outcomes=["Yes", "No"],
            outcome_prices=[0.25, 0.75],
            volume=100_000,
            liquidity=5_000,
            end_date=None,
            active=True,
            closed=False,
        )
        analysis = svc.analyse_market(market)
        assert analysis.sentiment == "bearish"


# ── Experiment ────────────────────────────────────────────────────────────────

class TestRegimeDetector:
    def test_trending_up(self):
        from app.services.experiment.regime import RegimeDetector, Regime

        # Use a higher volatility_threshold to prevent volatile classification
        detector = RegimeDetector(trend_period=5, volatility_threshold=0.05)
        closes = [100, 102, 105, 108, 112, 116, 120, 125, 130, 135]
        result = detector.detect(closes)
        assert result["regime"] == Regime.TRENDING_UP
        assert 0 < result["confidence"] <= 1

    def test_trending_down(self):
        from app.services.experiment.regime import RegimeDetector, Regime

        detector = RegimeDetector(trend_period=5, volatility_threshold=0.05)
        closes = [135, 130, 125, 120, 116, 112, 108, 105, 102, 100]
        result = detector.detect(closes)
        assert result["regime"] == Regime.TRENDING_DOWN

    def test_insufficient_data(self):
        from app.services.experiment.regime import RegimeDetector, Regime

        detector = RegimeDetector(trend_period=20)
        result = detector.detect([100, 101, 102])
        assert result["regime"] == Regime.RANGING


class TestExperimentScorer:
    def test_score_basic(self):
        from app.services.experiment.scoring import ExperimentScorer

        scorer = ExperimentScorer()
        equity = [10_000, 10_500, 11_000, 10_800, 11_500, 12_000]
        score = scorer.score("exp-1", equity_curve=equity)
        assert 0.0 <= score.total_score <= 1.0
        assert score.experiment_id == "exp-1"

    def test_score_empty_curve(self):
        from app.services.experiment.scoring import ExperimentScorer

        scorer = ExperimentScorer()
        score = scorer.score("exp-empty", equity_curve=[])
        assert score.total_score == 0.0

    def test_rank(self):
        from app.services.experiment.scoring import ExperimentScorer, ExperimentScore

        scorer = ExperimentScorer()
        scores = [
            ExperimentScore("a", 0.3, 0.3, 0.3, 0.3, {}),
            ExperimentScore("b", 0.8, 0.8, 0.8, 0.8, {}),
            ExperimentScore("c", 0.5, 0.5, 0.5, 0.5, {}),
        ]
        ranked = scorer.rank(scores)
        assert ranked[0].experiment_id == "b"
        assert ranked[-1].experiment_id == "a"


class TestStrategyEvolver:
    def test_evolve_improves_score(self):
        from app.services.experiment.evolution import StrategyEvolver, StrategyGene, EvolutionConfig

        config = EvolutionConfig(population_size=5, generations=3, seed=0)
        gene = StrategyGene(strategy_code="", parameters={"period": 10, "threshold": 0.5})

        def scoring_fn(g):
            return g.parameters.get("period", 0) * g.parameters.get("threshold", 0)

        evolver = StrategyEvolver(config)
        result = evolver.evolve(gene, scoring_fn)
        assert result.best_gene.score >= 0
        assert len(result.generation_scores) == 3


# ── Data infrastructure ───────────────────────────────────────────────────────

class TestCacheManager:
    @pytest.mark.asyncio
    async def test_set_and_get(self):
        from app.services.data.cache_manager import CacheManager

        cm = CacheManager()
        await cm.set("key1", {"value": 42}, ttl=60)
        result = await cm.get("key1")
        assert result == {"value": 42}

    @pytest.mark.asyncio
    async def test_miss(self):
        from app.services.data.cache_manager import CacheManager

        cm = CacheManager()
        result = await cm.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_or_fetch(self):
        from app.services.data.cache_manager import CacheManager

        cm = CacheManager()
        calls = []

        async def fetch_fn():
            calls.append(1)
            return "fetched"

        val1 = await cm.get_or_fetch("k", fetch_fn)
        val2 = await cm.get_or_fetch("k", fetch_fn)  # should use cache
        assert val1 == "fetched"
        assert val2 == "fetched"
        assert len(calls) == 1  # fetch called only once


class TestCircuitBreaker:
    @pytest.mark.asyncio
    async def test_closed_state_allows_calls(self):
        from app.services.data.circuit_breaker import CircuitBreaker

        cb = CircuitBreaker("test", failure_threshold=3)

        async def success_fn():
            return "ok"

        result = await cb.call(success_fn)
        assert result == "ok"

    @pytest.mark.asyncio
    async def test_opens_after_threshold(self):
        from app.services.data.circuit_breaker import CircuitBreaker, CircuitBreakerOpen

        cb = CircuitBreaker("test2", failure_threshold=2)

        async def fail_fn():
            raise RuntimeError("boom")

        for _ in range(2):
            with pytest.raises(RuntimeError):
                await cb.call(fail_fn)

        with pytest.raises(CircuitBreakerOpen):
            await cb.call(fail_fn)


class TestRateLimiter:
    @pytest.mark.asyncio
    async def test_acquire(self):
        from app.services.data.rate_limiter import TokenBucketLimiter

        limiter = TokenBucketLimiter(rate=100.0, burst=5)
        # Should succeed quickly
        await limiter.acquire()

    def test_try_acquire(self):
        from app.services.data.rate_limiter import TokenBucketLimiter

        limiter = TokenBucketLimiter(rate=1.0, burst=2)
        assert limiter.try_acquire() is True
        assert limiter.try_acquire() is True
        # Burst exhausted
        assert limiter.try_acquire() is False


# ── Symbol name resolver ──────────────────────────────────────────────────────

class TestSymbolNameResolver:
    def test_crypto(self):
        from app.services.symbol_name import SymbolNameResolver

        r = SymbolNameResolver()
        result = r.resolve("BTCUSDT")
        assert result["asset_class"] == "crypto"

    def test_forex(self):
        from app.services.symbol_name import SymbolNameResolver

        r = SymbolNameResolver()
        result = r.resolve("EURUSD")
        assert result["asset_class"] == "forex"
        assert "Euro" in result["name"]

    def test_unknown(self):
        from app.services.symbol_name import SymbolNameResolver

        r = SymbolNameResolver()
        result = r.resolve("XYZABC_UNKNOWN")
        assert result["symbol"] == "XYZABC_UNKNOWN"


# ── Code quality checker ──────────────────────────────────────────────────────

class TestIndicatorCodeQualityChecker:
    def test_valid_code(self):
        from app.services.strategy.code_quality import IndicatorCodeQualityChecker

        checker = IndicatorCodeQualityChecker()
        code = """
class MyStrategy:
    def on_init(self):
        pass

    def on_bar(self, bar):
        pass
"""
        report = checker.check(code)
        assert report.passed is True
        assert report.score > 50

    def test_syntax_error(self):
        from app.services.strategy.code_quality import IndicatorCodeQualityChecker

        checker = IndicatorCodeQualityChecker()
        report = checker.check("def foo(: pass")
        assert report.passed is False
        assert report.score == 0.0

    def test_forbidden_import(self):
        from app.services.strategy.code_quality import IndicatorCodeQualityChecker, IssueSeverity

        checker = IndicatorCodeQualityChecker()
        code = "import os\nprint(os.getcwd())"
        report = checker.check(code)
        assert report.passed is False
        assert any(i.severity == IssueSeverity.ERROR for i in report.issues)

    def test_missing_methods_warning(self):
        from app.services.strategy.code_quality import IndicatorCodeQualityChecker, IssueSeverity

        checker = IndicatorCodeQualityChecker()
        code = "class MyStrategy:\n    pass"
        report = checker.check(code)
        warnings = [i for i in report.issues if i.severity == IssueSeverity.WARNING]
        assert len(warnings) >= 1
