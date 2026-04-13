"""Data provider factory — returns the right provider for a given asset class."""

from __future__ import annotations

from typing import Literal

from app.services.data.providers.base import BaseDataProvider
from app.services.data.providers.crypto import CryptoDataProvider
from app.services.data.providers.forex import ForexDataProvider
from app.services.data.providers.stock import StockDataProvider

AssetClass = Literal["crypto", "forex", "stock", "futures", "polymarket"]

_registry: dict[str, type[BaseDataProvider]] = {
    "crypto": CryptoDataProvider,
    "forex": ForexDataProvider,
    "stock": StockDataProvider,
}

# Late-import optional providers to avoid hard dependency errors
def _register_optional() -> None:
    try:
        from app.services.data.providers.cn_stock import CnStockDataProvider
        _registry["cn_stock"] = CnStockDataProvider
    except ImportError:
        pass
    try:
        from app.services.data.providers.hk_stock import HkStockDataProvider
        _registry["hk_stock"] = HkStockDataProvider
    except ImportError:
        pass
    try:
        from app.services.data.providers.futures import FuturesDataProvider
        _registry["futures"] = FuturesDataProvider
    except ImportError:
        pass

_register_optional()


class DataProviderFactory:
    """Factory for creating ``BaseDataProvider`` instances by asset class."""

    _instances: dict[str, BaseDataProvider] = {}

    @classmethod
    def get(cls, asset_class: str) -> BaseDataProvider:
        """Return a shared (singleton) provider instance."""
        key = asset_class.lower()
        if key not in cls._instances:
            provider_cls = _registry.get(key)
            if provider_cls is None:
                raise ValueError(
                    f"No data provider registered for asset class '{key}'. "
                    f"Available: {list(_registry.keys())}"
                )
            cls._instances[key] = provider_cls()
        return cls._instances[key]

    @classmethod
    def register(cls, asset_class: str, provider: type[BaseDataProvider]) -> None:
        """Register a custom provider class under a new asset class key."""
        _registry[asset_class.lower()] = provider
        # Invalidate any cached instance
        cls._instances.pop(asset_class.lower(), None)

    @classmethod
    def available(cls) -> list[str]:
        """Return names of all registered asset classes."""
        return sorted(_registry.keys())
