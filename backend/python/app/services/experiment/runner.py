"""Experiment runner — orchestrates multi-step experiment pipelines."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    name: str
    strategy_code: str
    symbol: str
    timeframe: str = "1D"
    initial_capital: float = 10_000.0
    start_date: str = ""
    end_date: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    run_evolution: bool = False
    detect_regime: bool = True


@dataclass
class ExperimentResult:
    experiment_id: str
    config: ExperimentConfig
    backtest_result: dict[str, Any] | None = None
    evolution_result: dict[str, Any] | None = None
    regime_result: dict[str, Any] | None = None
    score_result: dict[str, Any] | None = None
    status: str = "pending"
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.config.name,
            "status": self.status,
            "backtest": self.backtest_result,
            "evolution": self.evolution_result,
            "regime": self.regime_result,
            "score": self.score_result,
            "error": self.error,
        }


class ExperimentRunner:
    """Run a complete experiment pipeline end-to-end."""

    async def run(self, config: ExperimentConfig) -> ExperimentResult:
        """Execute experiment steps based on config flags."""
        exp_id = str(uuid.uuid4())[:8]
        result = ExperimentResult(experiment_id=exp_id, config=config)

        try:
            result.status = "running"

            # Step 1: Backtest
            result.backtest_result = await self._run_backtest(config)

            # Step 2: Regime detection (optional)
            if config.detect_regime:
                result.regime_result = await self._detect_regime(config, result.backtest_result)

            # Step 3: Evolution (optional)
            if config.run_evolution:
                result.evolution_result = await self._run_evolution(config, result.backtest_result)

            # Step 4: Score
            result.score_result = self._score(exp_id, result.backtest_result)

            result.status = "completed"
            logger.info("Experiment %s completed successfully", exp_id)

        except Exception as exc:
            result.status = "failed"
            result.error = str(exc)
            logger.error("Experiment %s failed: %s", exp_id, exc)

        return result

    # ------------------------------------------------------------------
    # Internal steps
    # ------------------------------------------------------------------

    async def _run_backtest(self, config: ExperimentConfig) -> dict[str, Any]:
        from app.services.backtest.engine import BacktestEngine, BacktestConfig
        from app.services.strategy.script_strategy import Bar

        engine = BacktestEngine(
            BacktestConfig(initial_capital=config.initial_capital)
        )

        # Generate minimal synthetic bars for demo purposes
        # In production this would call the data provider
        bars = [
            Bar(
                timestamp=f"2024-01-{str(i + 1).zfill(2)}",
                open=100.0 + i,
                high=105.0 + i,
                low=95.0 + i,
                close=102.0 + i,
                volume=10_000.0,
            )
            for i in range(30)
        ]

        result = engine.run(bars, [], symbol=config.symbol)
        return result.to_dict() if hasattr(result, "to_dict") else {}

    async def _detect_regime(
        self, config: ExperimentConfig, backtest: dict[str, Any] | None
    ) -> dict[str, Any]:
        from app.services.experiment.regime import RegimeDetector

        equity = (backtest or {}).get("equity_curve", [])
        if len(equity) < 5:
            return {"regime": "ranging", "confidence": 0.5}

        detector = RegimeDetector()
        return detector.detect(closes=equity)

    async def _run_evolution(
        self, config: ExperimentConfig, backtest: dict[str, Any] | None
    ) -> dict[str, Any]:
        from app.services.experiment.evolution import StrategyEvolver, StrategyGene, EvolutionConfig

        base_gene = StrategyGene(
            strategy_code=config.strategy_code,
            parameters=config.parameters,
        )

        def scoring_fn(gene: StrategyGene) -> float:
            # Simple scoring based on parameter sum (placeholder for real backtest)
            return sum(float(v) for v in gene.parameters.values() if isinstance(v, (int, float)))

        evolver = StrategyEvolver(EvolutionConfig(population_size=5, generations=3))
        evo_result = evolver.evolve(base_gene, scoring_fn)
        return evo_result.to_dict()

    def _score(
        self, exp_id: str, backtest: dict[str, Any] | None
    ) -> dict[str, Any]:
        from app.services.experiment.scoring import ExperimentScorer

        equity = (backtest or {}).get("equity_curve", [])
        scorer = ExperimentScorer()
        score = scorer.score(experiment_id=exp_id, equity_curve=equity)
        return score.to_dict()
