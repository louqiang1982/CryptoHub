from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.redis import redis_manager
from app.api import ai_analysis, backtest, strategy_engine, indicator, code_gen, polymarket


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await redis_manager.connect()
    yield
    # Shutdown
    await redis_manager.disconnect()


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_analysis.router, prefix=f"{settings.API_PREFIX}/ai", tags=["AI Analysis"])
app.include_router(backtest.router, prefix=f"{settings.API_PREFIX}/backtest", tags=["Backtest"])
app.include_router(strategy_engine.router, prefix=f"{settings.API_PREFIX}/strategy", tags=["Strategy"])
app.include_router(indicator.router, prefix=f"{settings.API_PREFIX}/indicator", tags=["Indicators"])
app.include_router(code_gen.router, prefix=f"{settings.API_PREFIX}/codegen", tags=["Code Generation"])
app.include_router(polymarket.router, prefix=f"{settings.API_PREFIX}/polymarket", tags=["Polymarket"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}