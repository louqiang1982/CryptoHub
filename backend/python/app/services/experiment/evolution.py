"""Strategy evolution — iterative AI-driven improvement of strategy parameters.

Applies a simple genetic-style optimisation: generate parameter variants,
run backtests on each, score them, keep the best, repeat.
"""

from __future__ import annotations

import copy
import logging
import random
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class StrategyGene:
    """Mutable configuration for one strategy variant."""

    strategy_code: str
    parameters: dict[str, Any]
    generation: int = 0
    score: float = 0.0

    def mutate(self, mutation_rate: float = 0.1) -> "StrategyGene":
        """Return a mutated copy of this gene."""
        new_params = copy.deepcopy(self.parameters)
        for key, value in new_params.items():
            if isinstance(value, (int, float)) and random.random() < mutation_rate:
                # Apply ±20 % random perturbation
                delta = value * random.uniform(-0.2, 0.2)
                new_params[key] = type(value)(value + delta)
        return StrategyGene(
            strategy_code=self.strategy_code,
            parameters=new_params,
            generation=self.generation + 1,
        )


@dataclass
class EvolutionConfig:
    population_size: int = 10
    generations: int = 5
    mutation_rate: float = 0.15
    elite_fraction: float = 0.2  # top 20 % survive unchanged
    seed: int = 42


@dataclass
class EvolutionResult:
    best_gene: StrategyGene
    generation_scores: list[float] = field(default_factory=list)
    all_genes: list[StrategyGene] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "best_parameters": self.best_gene.parameters,
            "best_score": self.best_gene.score,
            "generations_run": self.best_gene.generation,
            "generation_scores": self.generation_scores,
        }


class StrategyEvolver:
    """Evolves strategy parameters over multiple generations."""

    def __init__(self, config: EvolutionConfig | None = None) -> None:
        self._cfg = config or EvolutionConfig()
        random.seed(self._cfg.seed)

    def evolve(
        self,
        base_gene: StrategyGene,
        scoring_fn: Any,  # Callable[[StrategyGene], float]
    ) -> EvolutionResult:
        """Run the evolution loop.

        Parameters
        ----------
        base_gene:
            Starting strategy configuration.
        scoring_fn:
            Callable that accepts a ``StrategyGene`` and returns a float
            score (higher is better).
        """
        population = [base_gene] + [
            base_gene.mutate(self._cfg.mutation_rate)
            for _ in range(self._cfg.population_size - 1)
        ]
        generation_scores: list[float] = []

        for gen in range(self._cfg.generations):
            # Score all
            for gene in population:
                try:
                    gene.score = float(scoring_fn(gene))
                except Exception as exc:
                    logger.warning("Scoring failed for gene: %s", exc)
                    gene.score = float("-inf")

            population.sort(key=lambda g: g.score, reverse=True)
            best_score = population[0].score
            generation_scores.append(best_score)
            logger.info("Generation %d/%d best score: %.4f", gen + 1, self._cfg.generations, best_score)

            # Elitism + mutation
            n_elite = max(1, int(len(population) * self._cfg.elite_fraction))
            elite = population[:n_elite]
            offspring = [
                random.choice(elite).mutate(self._cfg.mutation_rate)
                for _ in range(self._cfg.population_size - n_elite)
            ]
            population = elite + offspring

        best = max(population, key=lambda g: g.score)
        return EvolutionResult(
            best_gene=best,
            generation_scores=generation_scores,
            all_genes=population,
        )
