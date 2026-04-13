"""Web search service for AI-assisted analysis.

Wraps multiple search backends with a unified interface.  Supported
backends (tried in order):
1. DuckDuckGo Instant Answer API (no key required, free)
2. Serper API (requires SERPER_API_KEY env var)
3. Brave Search API (requires BRAVE_API_KEY env var)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
        }


class WebSearchService:
    """Multi-backend web search service.

    Falls back through available backends automatically.
    """

    def __init__(self, timeout: float = 10.0) -> None:
        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)
        self._serper_key = os.getenv("SERPER_API_KEY", "")
        self._brave_key = os.getenv("BRAVE_API_KEY", "")

    async def close(self) -> None:
        await self._client.aclose()

    async def search(
        self,
        query: str,
        num_results: int = 5,
    ) -> list[SearchResult]:
        """Run a web search and return top results.

        Tries backends in order: Serper → Brave → DuckDuckGo.
        """
        if self._serper_key:
            results = await self._serper_search(query, num_results)
            if results:
                return results

        if self._brave_key:
            results = await self._brave_search(query, num_results)
            if results:
                return results

        return await self._ddg_search(query, num_results)

    async def search_news(
        self, query: str, num_results: int = 5
    ) -> list[SearchResult]:
        """Search for recent news articles."""
        return await self.search(f"{query} news site:reuters.com OR site:bloomberg.com OR site:cnbc.com", num_results)

    # ------------------------------------------------------------------
    # Backend implementations
    # ------------------------------------------------------------------

    async def _serper_search(
        self, query: str, num_results: int
    ) -> list[SearchResult]:
        try:
            resp = await self._client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": self._serper_key, "Content-Type": "application/json"},
                json={"q": query, "num": num_results},
            )
            resp.raise_for_status()
            data = resp.json()
            organic = data.get("organic", [])
            return [
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="serper",
                )
                for item in organic[:num_results]
            ]
        except Exception as exc:
            logger.warning("Serper search failed: %s", exc)
            return []

    async def _brave_search(
        self, query: str, num_results: int
    ) -> list[SearchResult]:
        try:
            resp = await self._client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"Accept": "application/json", "X-Subscription-Token": self._brave_key},
                params={"q": query, "count": num_results},
            )
            resp.raise_for_status()
            data = resp.json()
            items = data.get("web", {}).get("results", [])
            return [
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", ""),
                    source="brave",
                )
                for item in items[:num_results]
            ]
        except Exception as exc:
            logger.warning("Brave search failed: %s", exc)
            return []

    async def _ddg_search(
        self, query: str, num_results: int
    ) -> list[SearchResult]:
        """DuckDuckGo instant answer API (no key required)."""
        try:
            resp = await self._client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"},
            )
            resp.raise_for_status()
            data = resp.json()

            results: list[SearchResult] = []
            # Abstract (main result)
            if data.get("AbstractText"):
                results.append(
                    SearchResult(
                        title=data.get("Heading", ""),
                        url=data.get("AbstractURL", ""),
                        snippet=data["AbstractText"],
                        source="duckduckgo",
                    )
                )
            # Related topics
            for topic in data.get("RelatedTopics", [])[:num_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(
                        SearchResult(
                            title=topic.get("Text", "")[:80],
                            url=topic.get("FirstURL", ""),
                            snippet=topic.get("Text", ""),
                            source="duckduckgo",
                        )
                    )
            return results[:num_results]
        except Exception as exc:
            logger.warning("DuckDuckGo search failed: %s", exc)
            return []
