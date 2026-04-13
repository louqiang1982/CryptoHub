"""USDT TRC20 payment service.

Handles USDT payments on the TRON network for membership purchases.
Uses the Tron Grid API (https://api.trongrid.io) to:
- Generate receiving addresses
- Verify incoming transactions
- Track payment status
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

import httpx

logger = logging.getLogger(__name__)

TRON_GRID_API = "https://api.trongrid.io"
USDT_TRC20_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # mainnet USDT TRC20


class PaymentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMING = "confirming"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"


@dataclass
class PaymentOrder:
    order_id: str
    user_id: str
    plan_id: str
    amount_usdt: float
    receiving_address: str
    tx_hash: str | None = None
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: float = 0.0
    confirmed_at: float | None = None
    expires_at: float = 0.0  # Unix timestamp

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = time.time()
        if not self.expires_at:
            self.expires_at = self.created_at + 3600  # 1 hour window

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "amount_usdt": self.amount_usdt,
            "receiving_address": self.receiving_address,
            "tx_hash": self.tx_hash,
            "status": self.status,
            "created_at": self.created_at,
            "confirmed_at": self.confirmed_at,
            "expires_at": self.expires_at,
        }


class UsdtPaymentService:
    """USDT TRC20 payment processor using Tron Grid REST API.

    Parameters
    ----------
    api_key:
        Tron Grid API key (optional — public endpoints work without it).
    required_confirmations:
        Number of block confirmations to consider a payment complete (default 20).
    """

    def __init__(
        self,
        api_key: str = "",
        required_confirmations: int = 20,
    ) -> None:
        self._api_key = api_key or os.getenv("TRON_GRID_API_KEY", "")
        self._required_confirmations = required_confirmations
        headers: dict[str, str] = {"Accept": "application/json"}
        if self._api_key:
            headers["TRON-PRO-API-KEY"] = self._api_key
        self._client = httpx.AsyncClient(
            base_url=TRON_GRID_API,
            headers=headers,
            timeout=15.0,
        )

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------------

    def generate_order_id(self, user_id: str, plan_id: str) -> str:
        """Generate a unique order ID."""
        raw = f"{user_id}:{plan_id}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

    async def create_payment_order(
        self,
        user_id: str,
        plan_id: str,
        amount_usdt: float,
        receiving_address: str,
    ) -> PaymentOrder:
        """Create a new payment order for a membership plan."""
        order_id = self.generate_order_id(user_id, plan_id)
        order = PaymentOrder(
            order_id=order_id,
            user_id=user_id,
            plan_id=plan_id,
            amount_usdt=amount_usdt,
            receiving_address=receiving_address,
        )
        logger.info(
            "Created USDT payment order %s for user %s, amount %.2f USDT",
            order_id,
            user_id,
            amount_usdt,
        )
        return order

    # ------------------------------------------------------------------
    # Transaction verification
    # ------------------------------------------------------------------

    async def verify_payment(
        self, order: PaymentOrder
    ) -> PaymentOrder:
        """Check Tron Grid for a completed USDT transfer matching this order."""
        if order.is_expired():
            order.status = PaymentStatus.EXPIRED
            return order

        try:
            resp = await self._client.get(
                f"/v1/accounts/{order.receiving_address}/transactions/trc20",
                params={
                    "limit": 20,
                    "contract_address": USDT_TRC20_CONTRACT,
                    "only_to": "true",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            txns = data.get("data", [])

            for tx in txns:
                value = int(tx.get("value", "0")) / 1_000_000  # 6 decimals
                to_addr = tx.get("to", "")
                confirmations = tx.get("confirmations", 0)

                if (
                    to_addr == order.receiving_address
                    and abs(value - order.amount_usdt) < 0.01  # allow 0.01 USDT tolerance
                ):
                    if confirmations >= self._required_confirmations:
                        order.tx_hash = tx.get("transaction_id")
                        order.status = PaymentStatus.COMPLETED
                        order.confirmed_at = time.time()
                        logger.info(
                            "Payment order %s confirmed (tx: %s)",
                            order.order_id,
                            order.tx_hash,
                        )
                    else:
                        order.status = PaymentStatus.CONFIRMING
                        order.tx_hash = tx.get("transaction_id")
                    return order

        except Exception as exc:
            logger.error("Payment verification error for order %s: %s", order.order_id, exc)

        return order

    async def get_transaction(self, tx_hash: str) -> dict[str, Any]:
        """Fetch full transaction details from Tron Grid."""
        try:
            resp = await self._client.post(
                "/wallet/gettransactionbyid",
                json={"value": tx_hash},
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Failed to fetch transaction %s: %s", tx_hash, exc)
            return {}
