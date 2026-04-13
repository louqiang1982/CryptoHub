"""Polymarket prediction-market research service.

Provides fetching, analysis and batch analysis of Polymarket prediction
markets.  Uses the Polymarket REST API (https://gamma-api.polymarket.com).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

import httpx

logger = logging.getLogger(__name__)

POLYMARKET_API = "https://gamma-api.polymarket.com"
DEFAULT_LIMIT = 50


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class Market:
    """A single Polymarket prediction market."""

    market_id: str
    question: str
    outcomes: list[str]
    outcome_prices: list[float]
    volume: float
    liquidity: float
    end_date: str | None
    active: bool
    closed: bool
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Market":
        tokens = data.get("tokens", [])
        outcomes = [t.get("outcome", "") for t in tokens]
        prices = [float(t.get("price", 0)) for t in tokens]
        return cls(
            market_id=data.get("conditionId", data.get("id", "")),
            question=data.get("question", ""),
            outcomes=outcomes,
            outcome_prices=prices,
            volume=float(data.get("volume", 0)),
            liquidity=float(data.get("liquidity", 0)),
            end_date=data.get("endDateIso"),
            active=bool(data.get("active", False)),
            closed=bool(data.get("closed", False)),
            tags=[t.get("slug", "") for t in data.get("tags", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "market_id": self.market_id,
            "question": self.question,
            "outcomes": self.outcomes,
            "outcome_prices": self.outcome_prices,
            "volume": self.volume,
            "liquidity": self.liquidity,
            "end_date": self.end_date,
            "active": self.active,
            "closed": self.closed,
            "tags": self.tags,
        }


@dataclass
class MarketAnalysis:
    """AI-generated analysis for a Polymarket market."""

    market_id: str
    question: str
    implied_probabilities: dict[str, float]
    sentiment: str  # "bullish" | "bearish" | "neutral"
    confidence: float  # 0–1
    summary: str
    notable_moves: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "market_id": self.market_id,
            "question": self.question,
            "implied_probabilities": self.implied_probabilities,
            "sentiment": self.sentiment,
            "confidence": self.confidence,
            "summary": self.summary,
            "notable_moves": self.notable_moves,
        }


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class PolymarketService:
    """Fetches and analyses Polymarket prediction markets.

    Sentiment classification thresholds:
    - ``BULLISH_THRESHOLD`` (0.60): When the leading outcome probability ≥ 60 %,
      consensus leans strongly towards resolution, classified as bullish.
    - ``BEARISH_THRESHOLD`` (0.40): When the probability ≤ 40 %, the market
      leans against the outcome, classified as bearish.
    - Between 40 % and 60 %: classified as neutral (market is undecided).
    These thresholds mirror standard options-market convention where ±20 pp
    from the 50 % midpoint represents a directional lean.
    """

    BULLISH_THRESHOLD: float = 0.60
    BEARISH_THRESHOLD: float = 0.40

    def __init__(self, timeout: float = 15.0) -> None:
        self._client = httpx.AsyncClient(
            base_url=POLYMARKET_API,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Market fetching
    # ------------------------------------------------------------------

    async def get_markets(
        self,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
        tag: str | None = None,
        active: bool = True,
    ) -> list[Market]:
        """Return active prediction markets, optionally filtered by tag."""
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "active": "true" if active else "false",
        }
        if tag:
            params["tag"] = tag

        try:
            resp = await self._client.get("/markets", params=params)
            resp.raise_for_status()
            data = resp.json()
            items = data if isinstance(data, list) else data.get("data", [])
            return [Market.from_dict(m) for m in items]
        except Exception as exc:
            logger.warning("Failed to fetch Polymarket markets: %s", exc)
            return []

    async def get_market(self, market_id: str) -> Market | None:
        """Fetch a single market by condition ID."""
        try:
            resp = await self._client.get(f"/markets/{market_id}")
            resp.raise_for_status()
            return Market.from_dict(resp.json())
        except Exception as exc:
            logger.warning("Failed to fetch market %s: %s", market_id, exc)
            return None

    async def get_trending_markets(self, limit: int = 20) -> list[Market]:
        """Return markets sorted by 24 h volume descending."""
        markets = await self.get_markets(limit=limit * 2)
        return sorted(markets, key=lambda m: m.volume, reverse=True)[:limit]

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def analyse_market(self, market: Market) -> MarketAnalysis:
        """Generate a simple rule-based analysis for a market."""
        probs: dict[str, float] = {}
        for outcome, price in zip(market.outcomes, market.outcome_prices):
            probs[outcome] = round(price * 100, 2)

        # Simple sentiment: if the first (usually "Yes") outcome ≥ BULLISH_THRESHOLD → bullish
        first_price = market.outcome_prices[0] if market.outcome_prices else 0.5
        if first_price >= self.BULLISH_THRESHOLD:
            sentiment = "bullish"
            confidence = first_price
        elif first_price <= self.BEARISH_THRESHOLD:
            sentiment = "bearish"
            confidence = 1 - first_price
        else:
            sentiment = "neutral"
            confidence = 0.5

        notable_moves: list[str] = []
        if market.volume > 100_000:
            notable_moves.append(f"High volume: ${market.volume:,.0f}")
        if market.liquidity > 50_000:
            notable_moves.append(f"High liquidity: ${market.liquidity:,.0f}")

        summary = (
            f"{market.question} — Implied probability of "
            f"'{market.outcomes[0] if market.outcomes else 'Yes'}': "
            f"{probs.get(market.outcomes[0] if market.outcomes else 'Yes', 0):.1f}%."
        )

        return MarketAnalysis(
            market_id=market.market_id,
            question=market.question,
            implied_probabilities=probs,
            sentiment=sentiment,
            confidence=round(confidence, 3),
            summary=summary,
            notable_moves=notable_moves,
        )


# ---------------------------------------------------------------------------
# Batch analyser
# ---------------------------------------------------------------------------


class PolymarketBatchAnalyser:
    """Run PolymarketService analysis across many markets at once."""

    def __init__(self, service: PolymarketService | None = None) -> None:
        self._svc = service or PolymarketService()

    async def analyse_trending(
        self, limit: int = 20
    ) -> list[MarketAnalysis]:
        """Fetch trending markets and return analyses."""
        markets = await self._svc.get_trending_markets(limit=limit)
        return [self._svc.analyse_market(m) for m in markets]

    async def analyse_by_ids(
        self, market_ids: list[str]
    ) -> list[MarketAnalysis]:
        """Fetch and analyse specific markets by ID."""
        results: list[MarketAnalysis] = []
        for mid in market_ids:
            market = await self._svc.get_market(mid)
            if market:
                results.append(self._svc.analyse_market(market))
        return results
