"""Prompt management for AI experiment workflows.

Centralises all LLM prompts used in experiment modules so they can be
versioned, tested and swapped without touching service logic.
"""

from __future__ import annotations

from string import Template
from typing import Any


class PromptRegistry:
    """Registry of named prompt templates."""

    _templates: dict[str, Template] = {}

    @classmethod
    def register(cls, name: str, template: str) -> None:
        cls._templates[name] = Template(template)

    @classmethod
    def render(cls, name: str, **kwargs: Any) -> str:
        tmpl = cls._templates.get(name)
        if tmpl is None:
            raise KeyError(f"Prompt '{name}' not registered")
        return tmpl.safe_substitute(**kwargs)

    @classmethod
    def list_names(cls) -> list[str]:
        return list(cls._templates.keys())


# ------------------------------------------------------------------
# Built-in prompts
# ------------------------------------------------------------------

PromptRegistry.register(
    "strategy_analysis",
    """You are a quantitative trading expert.
Analyse the following strategy and provide detailed feedback.

Strategy code:
```python
$strategy_code
```

Current parameters: $parameters

Historical performance:
- Total return: $total_return%
- Sharpe ratio: $sharpe
- Max drawdown: $max_drawdown%

Provide:
1. Strategy strengths and weaknesses
2. Parameter improvement suggestions
3. Risk management recommendations
4. Market regime suitability analysis
""",
)

PromptRegistry.register(
    "regime_commentary",
    """Given the following market regime data for $symbol:

Detected regime: $regime
Confidence: $confidence
EMA slope: $ema_slope
ATR ratio: $atr_ratio

Write a concise 2–3 sentence market commentary suitable for a trading dashboard.
Focus on actionable implications for strategy selection.
""",
)

PromptRegistry.register(
    "evolution_summary",
    """A strategy evolution run has completed with the following results:

Generations run: $generations
Best score achieved: $best_score
Initial score: $initial_score
Improvement: $improvement%

Best parameters found: $best_parameters

Summarise the evolution results in plain language, highlighting:
1. Which parameters changed most significantly
2. The improvement in risk-adjusted performance
3. Suggested next steps for further optimisation
""",
)

PromptRegistry.register(
    "experiment_report",
    """Generate a professional experiment report for the following trading strategy experiment:

Experiment ID: $experiment_id
Strategy: $strategy_name
Asset: $symbol
Timeframe: $timeframe
Period tested: $start_date to $end_date

Performance metrics:
- Total return: $total_return%
- Sharpe ratio: $sharpe
- Sortino ratio: $sortino
- Max drawdown: $max_drawdown%
- Win rate: $win_rate%
- Total trades: $num_trades

Provide a structured report with executive summary, key findings, and recommendations.
""",
)
