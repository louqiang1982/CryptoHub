"""MetaTrader 5 (MT5) live-trading adapter.

Wraps the official `MetaTrader5` Python package which requires a running
MT5 terminal process.  This module provides a clean async-friendly
interface and falls back gracefully when the package is not installed (e.g.
in test / CI environments).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

try:
    import MetaTrader5 as _mt5  # type: ignore[import]

    MT5_AVAILABLE = True
except ImportError:
    _mt5 = None  # type: ignore[assignment]
    MT5_AVAILABLE = False
    logger.warning(
        "MetaTrader5 package not installed – MT5Adapter will run in stub mode"
    )


# ---------------------------------------------------------------------------
# Config / data models
# ---------------------------------------------------------------------------


@dataclass
class MT5Config:
    """Connection settings for the MT5 terminal."""

    server: str = ""
    login: int = 0
    password: str = ""
    timeout: int = 60_000  # ms


@dataclass
class MT5Position:
    ticket: int
    symbol: str
    position_type: str  # "BUY" or "SELL"
    volume: float
    open_price: float
    current_price: float
    profit: float
    swap: float
    comment: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticket": self.ticket,
            "symbol": self.symbol,
            "type": self.position_type,
            "volume": self.volume,
            "open_price": self.open_price,
            "current_price": self.current_price,
            "profit": self.profit,
            "swap": self.swap,
            "comment": self.comment,
        }


@dataclass
class MT5Order:
    symbol: str
    order_type: str  # "BUY", "SELL", "BUY_LIMIT", "SELL_LIMIT", …
    volume: float
    price: float = 0.0
    sl: float = 0.0  # stop-loss
    tp: float = 0.0  # take-profit
    deviation: int = 20  # max slippage in points
    magic: int = 0
    comment: str = ""


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------


class MT5Adapter:
    """Thin async-compatible wrapper around the MetaTrader5 package."""

    def __init__(self, config: MT5Config | None = None) -> None:
        self._cfg = config or MT5Config()
        self._connected = False

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        """Initialise the MT5 terminal connection."""
        if not MT5_AVAILABLE:
            logger.warning("MT5 not available – running in stub mode")
            return False
        ok = _mt5.initialize(
            server=self._cfg.server or None,
            login=self._cfg.login or None,
            password=self._cfg.password or None,
            timeout=self._cfg.timeout,
        )
        if not ok:
            logger.error("MT5 initialise failed: %s", _mt5.last_error())
        self._connected = ok
        return ok

    def disconnect(self) -> None:
        """Shutdown MT5 connection."""
        if MT5_AVAILABLE and self._connected:
            _mt5.shutdown()
            self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def get_account_info(self) -> dict[str, Any]:
        """Return account balance, equity, margin details."""
        if not MT5_AVAILABLE or not self._connected:
            return {}
        info = _mt5.account_info()
        if info is None:
            return {}
        return {
            "login": info.login,
            "name": info.name,
            "server": info.server,
            "balance": info.balance,
            "equity": info.equity,
            "margin": info.margin,
            "margin_free": info.margin_free,
            "margin_level": info.margin_level,
            "currency": info.currency,
        }

    # ------------------------------------------------------------------
    # Positions
    # ------------------------------------------------------------------

    def get_positions(self, symbol: str | None = None) -> list[MT5Position]:
        """Return all open positions, optionally filtered by symbol."""
        if not MT5_AVAILABLE or not self._connected:
            return []
        raw = (
            _mt5.positions_get(symbol=symbol)
            if symbol
            else _mt5.positions_get()
        )
        if raw is None:
            return []
        return [
            MT5Position(
                ticket=p.ticket,
                symbol=p.symbol,
                position_type="BUY" if p.type == 0 else "SELL",
                volume=p.volume,
                open_price=p.price_open,
                current_price=p.price_current,
                profit=p.profit,
                swap=p.swap,
                comment=p.comment,
            )
            for p in raw
        ]

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def place_order(self, order: MT5Order) -> dict[str, Any]:
        """Submit a market or pending order."""
        if not MT5_AVAILABLE or not self._connected:
            raise RuntimeError("MT5 not connected")

        type_map = {
            "BUY": _mt5.ORDER_TYPE_BUY,
            "SELL": _mt5.ORDER_TYPE_SELL,
            "BUY_LIMIT": _mt5.ORDER_TYPE_BUY_LIMIT,
            "SELL_LIMIT": _mt5.ORDER_TYPE_SELL_LIMIT,
            "BUY_STOP": _mt5.ORDER_TYPE_BUY_STOP,
            "SELL_STOP": _mt5.ORDER_TYPE_SELL_STOP,
        }
        order_type = type_map.get(order.order_type.upper(), _mt5.ORDER_TYPE_BUY)

        request = {
            "action": _mt5.TRADE_ACTION_DEAL,
            "symbol": order.symbol,
            "volume": order.volume,
            "type": order_type,
            "price": order.price or _mt5.symbol_info_tick(order.symbol).ask,
            "sl": order.sl,
            "tp": order.tp,
            "deviation": order.deviation,
            "magic": order.magic,
            "comment": order.comment,
            "type_time": _mt5.ORDER_TIME_GTC,
            "type_filling": _mt5.ORDER_FILLING_IOC,
        }
        result = _mt5.order_send(request)
        if result is None or result.retcode != _mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(
                f"MT5 order failed: {result.retcode if result else 'None'}"
            )
        return {
            "order": result.order,
            "volume": result.volume,
            "price": result.price,
            "retcode": result.retcode,
        }

    def cancel_order(self, ticket: int) -> bool:
        """Cancel a pending order by ticket number."""
        if not MT5_AVAILABLE or not self._connected:
            raise RuntimeError("MT5 not connected")
        request = {
            "action": _mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
        }
        result = _mt5.order_send(request)
        return result is not None and result.retcode == _mt5.TRADE_RETCODE_DONE

    def close_position(self, ticket: int) -> dict[str, Any]:
        """Close an open position by ticket."""
        if not MT5_AVAILABLE or not self._connected:
            raise RuntimeError("MT5 not connected")
        positions = _mt5.positions_get()
        pos = next((p for p in (positions or []) if p.ticket == ticket), None)
        if pos is None:
            raise ValueError(f"Position {ticket} not found")

        order_type = _mt5.ORDER_TYPE_SELL if pos.type == 0 else _mt5.ORDER_TYPE_BUY
        tick = _mt5.symbol_info_tick(pos.symbol)
        price = tick.bid if pos.type == 0 else tick.ask

        request = {
            "action": _mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": pos.magic,
            "comment": "close",
            "type_time": _mt5.ORDER_TIME_GTC,
            "type_filling": _mt5.ORDER_FILLING_IOC,
        }
        result = _mt5.order_send(request)
        if result is None or result.retcode != _mt5.TRADE_RETCODE_DONE:
            raise RuntimeError(f"MT5 close failed: {result}")
        return {"order": result.order, "retcode": result.retcode}

    # ------------------------------------------------------------------
    # Market data
    # ------------------------------------------------------------------

    def get_symbol_info(self, symbol: str) -> dict[str, Any]:
        """Return symbol specification (digits, point, spread, etc.)."""
        if not MT5_AVAILABLE or not self._connected:
            return {}
        info = _mt5.symbol_info(symbol)
        if info is None:
            return {}
        return {
            "symbol": info.name,
            "digits": info.digits,
            "point": info.point,
            "spread": info.spread,
            "bid": info.bid,
            "ask": info.ask,
            "volume_min": info.volume_min,
            "volume_max": info.volume_max,
            "volume_step": info.volume_step,
        }

    def get_rates(
        self,
        symbol: str,
        timeframe: int = 16385,  # TIMEFRAME_D1
        count: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch OHLCV bars (copy_rates_from_pos)."""
        if not MT5_AVAILABLE or not self._connected:
            return []
        rates = _mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            return []
        return [
            {
                "time": int(r["time"]),
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "tick_volume": int(r["tick_volume"]),
            }
            for r in rates
        ]
