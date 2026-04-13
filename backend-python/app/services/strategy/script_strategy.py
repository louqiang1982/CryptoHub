"""Event-driven script strategy with on_init/on_bar lifecycle."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Order:
    side: str
    symbol: str
    quantity: float
    price: float | None = None
    order_type: str = "market"
    status: str = "pending"


class ScriptStrategy(ABC):
    """Base class for event-driven trading strategies."""

    def __init__(self, symbol: str, parameters: dict | None = None):
        self.symbol = symbol
        self.parameters = parameters or {}
        self.position: float = 0.0
        self.orders: list[Order] = []
        self.bars: list[Bar] = []
        self.variables: dict[str, Any] = {}

    @abstractmethod
    def on_init(self) -> None:
        """Called once when strategy starts."""
        pass

    @abstractmethod
    def on_bar(self, bar: Bar) -> None:
        """Called on each new bar/candle."""
        pass

    def buy(self, quantity: float, price: float | None = None) -> Order:
        order = Order(side="buy", symbol=self.symbol, quantity=quantity, price=price)
        self.orders.append(order)
        return order

    def sell(self, quantity: float, price: float | None = None) -> Order:
        order = Order(side="sell", symbol=self.symbol, quantity=quantity, price=price)
        self.orders.append(order)
        return order

    def run(self, bars: list[Bar]) -> list[Order]:
        self.on_init()
        for bar in bars:
            self.bars.append(bar)
            self.on_bar(bar)
        return self.orders
