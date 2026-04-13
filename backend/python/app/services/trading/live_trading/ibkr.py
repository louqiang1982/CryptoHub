"""Interactive Brokers (IBKR) live-trading adapter.

Uses the IBKR Client Portal Gateway REST API (port 5000 by default) so
that no native TWS/IB-Gateway install is required at runtime.  For
production use the *ib_insync* library can be substituted – just replace
the HTTP calls with the equivalent ib_insync equivalents.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass
class IBKRConfig:
    gateway_url: str = "https://localhost:5000/v1/api"
    verify_ssl: bool = False  # Gateway uses self-signed cert by default
    timeout: float = 30.0


@dataclass
class IBKROrder:
    account_id: str
    conid: int  # IBKR contract ID
    order_type: str  # MKT, LMT, STP …
    side: str  # BUY or SELL
    quantity: float
    price: float | None = None
    tif: str = "DAY"  # Time in force
    order_id: str | None = None


@dataclass
class IBKRPosition:
    conid: int
    symbol: str
    position: float
    avg_cost: float
    market_price: float
    unrealized_pnl: float
    realized_pnl: float
    currency: str = "USD"
    account_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "conid": self.conid,
            "symbol": self.symbol,
            "position": self.position,
            "avg_cost": self.avg_cost,
            "market_price": self.market_price,
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl,
            "currency": self.currency,
            "account_id": self.account_id,
        }


class IBKRAdapter:
    """REST-based adapter for Interactive Brokers Client Portal Gateway."""

    def __init__(self, config: IBKRConfig | None = None) -> None:
        self._cfg = config or IBKRConfig()
        self._client = httpx.AsyncClient(
            base_url=self._cfg.gateway_url,
            verify=self._cfg.verify_ssl,
            timeout=self._cfg.timeout,
        )
        self._account_id: str | None = None

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Session / authentication
    # ------------------------------------------------------------------

    async def authenticate(self) -> bool:
        """Authenticate with the Client Portal Gateway."""
        try:
            resp = await self._client.post("/iserver/auth/ssodh/init", json={})
            resp.raise_for_status()
            return True
        except Exception as exc:
            logger.error("IBKR authentication failed: %s", exc)
            return False

    async def keep_alive(self) -> bool:
        """Tickle session to prevent timeout."""
        try:
            resp = await self._client.post("/tickle")
            return resp.status_code == 200
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    async def get_accounts(self) -> list[str]:
        """Return list of account IDs."""
        try:
            resp = await self._client.get("/iserver/accounts")
            resp.raise_for_status()
            data = resp.json()
            accounts = data.get("accounts", [])
            if accounts and self._account_id is None:
                self._account_id = accounts[0]
            return accounts
        except Exception as exc:
            logger.error("Failed to get IBKR accounts: %s", exc)
            return []

    async def get_portfolio_summary(
        self, account_id: str | None = None
    ) -> dict[str, Any]:
        """Return portfolio-level summary (NAV, cash, etc.)."""
        acct = account_id or self._account_id or ""
        try:
            resp = await self._client.get(
                f"/portfolio/{acct}/summary"
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Failed to get portfolio summary: %s", exc)
            return {}

    # ------------------------------------------------------------------
    # Positions
    # ------------------------------------------------------------------

    async def get_positions(
        self, account_id: str | None = None, page: int = 0
    ) -> list[IBKRPosition]:
        """Fetch open positions for an account."""
        acct = account_id or self._account_id or ""
        try:
            resp = await self._client.get(
                f"/portfolio/{acct}/positions/{page}"
            )
            resp.raise_for_status()
            raw: list[dict] = resp.json()
            return [
                IBKRPosition(
                    conid=p.get("conid", 0),
                    symbol=p.get("contractDesc", ""),
                    position=float(p.get("position", 0)),
                    avg_cost=float(p.get("avgCost", 0)),
                    market_price=float(p.get("mktPrice", 0)),
                    unrealized_pnl=float(p.get("unrealizedPnl", 0)),
                    realized_pnl=float(p.get("realizedPnl", 0)),
                    currency=p.get("currency", "USD"),
                    account_id=acct,
                )
                for p in raw
            ]
        except Exception as exc:
            logger.error("Failed to get IBKR positions: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    async def place_order(self, order: IBKROrder) -> dict[str, Any]:
        """Submit an order to IBKR."""
        payload = {
            "orders": [
                {
                    "conid": order.conid,
                    "orderType": order.order_type,
                    "side": order.side,
                    "quantity": order.quantity,
                    "tif": order.tif,
                    **({"price": order.price} if order.price is not None else {}),
                }
            ]
        }
        try:
            resp = await self._client.post(
                f"/iserver/account/{order.account_id}/orders", json=payload
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Failed to place IBKR order: %s", exc)
            raise

    async def cancel_order(
        self, account_id: str, order_id: str
    ) -> dict[str, Any]:
        """Cancel a live order."""
        try:
            resp = await self._client.delete(
                f"/iserver/account/{account_id}/order/{order_id}"
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Failed to cancel IBKR order %s: %s", order_id, exc)
            raise

    async def get_live_orders(self) -> list[dict[str, Any]]:
        """Return all live (open) orders."""
        try:
            resp = await self._client.get("/iserver/account/orders")
            resp.raise_for_status()
            data = resp.json()
            return data.get("orders", [])
        except Exception as exc:
            logger.error("Failed to get IBKR live orders: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Market data (snapshot)
    # ------------------------------------------------------------------

    async def get_market_snapshot(
        self, conids: list[int], fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Fetch market-data snapshot for a list of contract IDs."""
        conid_str = ",".join(str(c) for c in conids)
        field_str = ",".join(fields or ["31", "84", "86", "88"])
        try:
            resp = await self._client.get(
                "/iserver/marketdata/snapshot",
                params={"conids": conid_str, "fields": field_str},
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Failed to get IBKR market snapshot: %s", exc)
            return []

    async def search_contract(self, symbol: str) -> list[dict[str, Any]]:
        """Search for a contract by symbol string."""
        try:
            resp = await self._client.get(
                "/iserver/secdef/search", params={"symbol": symbol}
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("IBKR contract search failed for %s: %s", symbol, exc)
            return []
