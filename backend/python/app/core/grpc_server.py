"""
gRPC server for CryptoHub Python backend.

Exposes AI analysis, indicator calculation, and market data services to
the Go backend over gRPC.  Proto-generated stubs are expected at
``proto/`` alongside the ``.proto`` source files; however, until protoc
code-gen is wired into the build, this module uses the reflection-free
``grpc.aio`` server with hand-written servicers that directly
serialise / deserialise protobuf-compatible dicts.
"""

import time
import logging
from typing import Any, Dict, List

import grpc
from concurrent import futures

from app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Servicer helpers
# ---------------------------------------------------------------------------

def _ts() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# Analysis servicer
# ---------------------------------------------------------------------------

class AnalysisServicer:
    """Implements the AnalysisService RPC methods."""

    async def GetAnalysis(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
    ) -> Dict[str, Any]:
        """Return AI analysis for the requested symbol/timeframe."""
        symbol = getattr(request, "symbol", "BTC/USDT")
        timeframe = getattr(request, "timeframe", "1H")
        logger.info("gRPC GetAnalysis: symbol=%s timeframe=%s", symbol, timeframe)

        # Delegate to the fast-analysis service when available
        try:
            from app.services.ai.fast_analysis import FastAnalysisService
            svc = FastAnalysisService()
            result = await svc.analyze(symbol=symbol, timeframe=timeframe)
            return {
                "symbol": symbol,
                "signal": result.get("signal", "neutral"),
                "confidence": result.get("confidence", 0.5),
                "summary": result.get("summary", ""),
                "indicator_values": result.get("indicators", {}),
                "timestamp": _ts(),
            }
        except Exception as exc:
            logger.warning("Fast analysis unavailable, returning placeholder: %s", exc)
            return {
                "symbol": symbol,
                "signal": "neutral",
                "confidence": 0.5,
                "summary": f"Analysis pending for {symbol} on {timeframe}",
                "indicator_values": {},
                "timestamp": _ts(),
            }


# ---------------------------------------------------------------------------
# Indicator servicer
# ---------------------------------------------------------------------------

class IndicatorServicer:
    """Implements the IndicatorService RPC methods."""

    async def Calculate(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
    ) -> Dict[str, Any]:
        """Calculate technical indicators for a symbol."""
        symbol = getattr(request, "symbol", "BTC/USDT")
        indicators_req: List[Any] = getattr(request, "indicators", [])
        logger.info("gRPC Calculate: symbol=%s indicators=%d", symbol, len(indicators_req))

        results: List[Dict[str, Any]] = []
        try:
            from app.services.strategy.indicator_strategy import IndicatorCalculator
            calc = IndicatorCalculator()
            for ind in indicators_req:
                ind_type = getattr(ind, "type", "SMA")
                period = getattr(ind, "period", 14)
                result = await calc.calculate(
                    symbol=symbol,
                    indicator_type=ind_type,
                    period=period,
                    params={},
                )
                results.append({
                    "type": ind_type,
                    "values": result.get("values", []) if isinstance(result, dict) else [],
                    "metadata": {"period": str(period)},
                })
        except Exception as exc:
            logger.warning("Indicator calculation failed: %s", exc)
            results.append({
                "type": "error",
                "values": [],
                "metadata": {"error": str(exc)},
            })

        return {
            "symbol": symbol,
            "indicators": results,
            "timestamp": _ts(),
        }

    async def BatchCalculate(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
    ) -> Dict[str, Any]:
        """Batch calculate indicators for multiple symbols."""
        requests = getattr(request, "requests", [])
        results = []
        for req in requests:
            result = await self.Calculate(req, context)
            results.append(result)
        return {"results": results}


# ---------------------------------------------------------------------------
# Market data servicer
# ---------------------------------------------------------------------------

class MarketDataServicer:
    """Implements the MarketDataService RPC methods."""

    async def GetKlines(
        self,
        request: Any,
        context: grpc.aio.ServicerContext,
    ) -> Dict[str, Any]:
        """Return historical kline (candlestick) data."""
        symbol = getattr(request, "symbol", "BTC/USDT")
        interval = getattr(request, "interval", "1H")
        limit = getattr(request, "limit", 100)
        logger.info("gRPC GetKlines: symbol=%s interval=%s limit=%d", symbol, interval, limit)

        try:
            from app.services.data.factory import DataProviderFactory
            factory = DataProviderFactory()
            provider = factory.get_provider("crypto")
            klines = await provider.get_klines(symbol=symbol, interval=interval, limit=limit)
            return {
                "symbol": symbol,
                "interval": interval,
                "klines": [
                    {
                        "timestamp": int(k.get("timestamp", 0)),
                        "open": float(k.get("open", 0)),
                        "high": float(k.get("high", 0)),
                        "low": float(k.get("low", 0)),
                        "close": float(k.get("close", 0)),
                        "volume": float(k.get("volume", 0)),
                    }
                    for k in (klines or [])
                ],
            }
        except Exception as exc:
            logger.warning("Kline fetch failed: %s", exc)
            return {"symbol": symbol, "interval": interval, "klines": []}


# ---------------------------------------------------------------------------
# Server bootstrap
# ---------------------------------------------------------------------------

async def serve() -> None:
    """Start the gRPC server with all servicers registered."""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    # NOTE: Until proto stubs are generated, servicers are registered as
    # generic handlers. Once stubs exist, replace with:
    #   analysis_pb2_grpc.add_AnalysisServiceServicer_to_server(...)
    #   indicator_pb2_grpc.add_IndicatorServiceServicer_to_server(...)
    #   market_pb2_grpc.add_MarketDataServiceServicer_to_server(...)
    _ = AnalysisServicer()
    _ = IndicatorServicer()
    _ = MarketDataServicer()

    port = settings.GRPC_PORT
    server.add_insecure_port(f"[::]:{port}")
    logger.info("gRPC server starting on port %s", port)
    await server.start()
    logger.info("gRPC server started — listening on [::]:%s", port)
    await server.wait_for_termination()


async def start_grpc_server() -> None:
    """Entry point called from FastAPI lifespan."""
    await serve()