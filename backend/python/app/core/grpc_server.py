"""
gRPC server for CryptoHub Python backend.

Exposes AI analysis, indicator calculation, and market data services to
the Go backend over gRPC using protoc-generated stubs located in the
top-level ``proto/`` directory.
"""

import sys
import os
import time
import logging
from typing import List

import grpc
from concurrent import futures

# Ensure the proto/ directory is on sys.path so generated _pb2 modules
# can be imported.
_PROTO_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "proto"))
if _PROTO_DIR not in sys.path:
    sys.path.insert(0, _PROTO_DIR)

import analysis_pb2  # noqa: E402
import analysis_pb2_grpc  # noqa: E402
import indicator_pb2  # noqa: E402
import indicator_pb2_grpc  # noqa: E402
import market_pb2  # noqa: E402
import market_pb2_grpc  # noqa: E402

from app.core.config import settings  # noqa: E402

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

class AnalysisServicer(analysis_pb2_grpc.AnalysisServiceServicer):
    """Implements the AnalysisService RPC methods."""

    async def GetAnalysis(
        self,
        request: analysis_pb2.AnalysisReq,
        context: grpc.aio.ServicerContext,
    ) -> analysis_pb2.AnalysisResp:
        """Return AI analysis for the requested symbol/timeframe."""
        symbol = request.symbol or "BTC/USDT"
        timeframe = request.timeframe or "1H"
        logger.info("gRPC GetAnalysis: symbol=%s timeframe=%s", symbol, timeframe)

        # Delegate to the fast-analysis service when available
        try:
            from app.services.ai.fast_analysis import FastAnalysisService
            svc = FastAnalysisService()
            result = await svc.analyze(symbol=symbol, timeframe=timeframe)
            return analysis_pb2.AnalysisResp(
                symbol=symbol,
                signal=result.get("signal", "neutral"),
                confidence=result.get("confidence", 0.5),
                summary=result.get("summary", ""),
                indicator_values={k: float(v) for k, v in result.get("indicators", {}).items()},
                timestamp=_ts(),
            )
        except Exception as exc:
            logger.warning("Fast analysis unavailable, returning placeholder: %s", exc)
            return analysis_pb2.AnalysisResp(
                symbol=symbol,
                signal="neutral",
                confidence=0.5,
                summary=f"Analysis pending for {symbol} on {timeframe}",
                indicator_values={},
                timestamp=_ts(),
            )

    async def StreamAnalysis(
        self,
        request: analysis_pb2.AnalysisReq,
        context: grpc.aio.ServicerContext,
    ):
        """Provide streaming analysis updates (sends a single snapshot)."""
        resp = await self.GetAnalysis(request, context)
        yield resp


# ---------------------------------------------------------------------------
# Indicator servicer
# ---------------------------------------------------------------------------

class IndicatorServicer(indicator_pb2_grpc.IndicatorServiceServicer):
    """Implements the IndicatorService RPC methods."""

    async def Calculate(
        self,
        request: indicator_pb2.IndicatorReq,
        context: grpc.aio.ServicerContext,
    ) -> indicator_pb2.IndicatorResp:
        """Calculate technical indicators for a symbol."""
        symbol = request.symbol or "BTC/USDT"
        indicators_req = list(request.indicators)
        logger.info("gRPC Calculate: symbol=%s indicators=%d", symbol, len(indicators_req))

        results: List[indicator_pb2.IndicatorValue] = []
        try:
            from app.services.strategy.indicator_strategy import IndicatorCalculator
            calc = IndicatorCalculator()
            for ind in indicators_req:
                ind_type = ind.type or "SMA"
                period = ind.period or 14
                result = await calc.calculate(
                    symbol=symbol,
                    indicator_type=ind_type,
                    period=period,
                    params={},
                )
                values = result.get("values", []) if isinstance(result, dict) else []
                results.append(indicator_pb2.IndicatorValue(
                    type=ind_type,
                    values=[float(v) for v in values],
                    metadata={"period": str(period)},
                ))
        except Exception as exc:
            logger.warning("Indicator calculation failed: %s", exc)
            results.append(indicator_pb2.IndicatorValue(
                type="error",
                values=[],
                metadata={"error": str(exc)},
            ))

        return indicator_pb2.IndicatorResp(
            symbol=symbol,
            indicators=results,
            timestamp=_ts(),
        )

    async def BatchCalculate(
        self,
        request: indicator_pb2.BatchIndicatorReq,
        context: grpc.aio.ServicerContext,
    ) -> indicator_pb2.BatchIndicatorResp:
        """Batch calculate indicators for multiple symbols."""
        results = []
        for req in request.requests:
            result = await self.Calculate(req, context)
            results.append(result)
        return indicator_pb2.BatchIndicatorResp(results=results)


# ---------------------------------------------------------------------------
# Market data servicer
# ---------------------------------------------------------------------------

class MarketDataServicer(market_pb2_grpc.MarketDataServiceServicer):
    """Implements the MarketDataService RPC methods."""

    async def GetKlines(
        self,
        request: market_pb2.KlineReq,
        context: grpc.aio.ServicerContext,
    ) -> market_pb2.KlineResp:
        """Return historical kline (candlestick) data."""
        symbol = request.symbol or "BTC/USDT"
        interval = request.interval or "1H"
        limit = request.limit or 100
        logger.info("gRPC GetKlines: symbol=%s interval=%s limit=%d", symbol, interval, limit)

        try:
            from app.services.data.factory import DataProviderFactory
            factory = DataProviderFactory()
            provider = factory.get_provider("crypto")
            klines = await provider.get_klines(symbol=symbol, interval=interval, limit=limit)
            return market_pb2.KlineResp(
                symbol=symbol,
                interval=interval,
                klines=[
                    market_pb2.Kline(
                        timestamp=int(k.get("timestamp", 0)),
                        open=float(k.get("open", 0)),
                        high=float(k.get("high", 0)),
                        low=float(k.get("low", 0)),
                        close=float(k.get("close", 0)),
                        volume=float(k.get("volume", 0)),
                    )
                    for k in (klines or [])
                ],
            )
        except Exception as exc:
            logger.warning("Kline fetch failed: %s", exc)
            return market_pb2.KlineResp(symbol=symbol, interval=interval, klines=[])

    async def SubscribeTicker(
        self,
        request: market_pb2.TickerReq,
        context: grpc.aio.ServicerContext,
    ):
        """Provide streaming ticker updates (sends a single snapshot per symbol)."""
        for sym in request.symbols:
            yield market_pb2.TickerUpdate(
                symbol=sym,
                price=0.0,
                change_24h=0.0,
                volume_24h=0.0,
                timestamp=int(time.time()),
            )


# ---------------------------------------------------------------------------
# Server bootstrap
# ---------------------------------------------------------------------------

async def serve() -> None:
    """Start the gRPC server with all servicers registered."""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    analysis_pb2_grpc.add_AnalysisServiceServicer_to_server(AnalysisServicer(), server)
    indicator_pb2_grpc.add_IndicatorServiceServicer_to_server(IndicatorServicer(), server)
    market_pb2_grpc.add_MarketDataServiceServicer_to_server(MarketDataServicer(), server)

    port = settings.GRPC_PORT
    server.add_insecure_port(f"[::]:{port}")
    logger.info("gRPC server starting on port %s", port)
    await server.start()
    logger.info("gRPC server started — listening on [::]:%s", port)
    await server.wait_for_termination()


async def start_grpc_server() -> None:
    """Entry point called from FastAPI lifespan."""
    await serve()