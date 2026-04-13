from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.strategy.compiler import StrategyCompiler
from app.services.strategy.runtime import StrategyRuntime
from app.schemas.strategy import StrategyRequest, StrategyResponse

router = APIRouter()


@router.post("/compile")
async def compile_strategy(request: StrategyRequest) -> Dict[str, Any]:
    """Compile and validate strategy code"""
    try:
        compiler = StrategyCompiler()
        result = await compiler.compile_and_validate(request.code)
        
        return {
            "valid": result.is_valid,
            "errors": result.errors,
            "warnings": result.warnings,
            "compiled_at": result.compiled_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/start")
async def start_live_strategy(request: StrategyRequest) -> Dict[str, str]:
    """Start live strategy execution"""
    try:
        runtime = StrategyRuntime()
        strategy_id = await runtime.start_strategy(
            code=request.code,
            symbol=request.symbol,
            parameters=request.parameters or {}
        )
        
        return {
            "strategy_id": strategy_id,
            "status": "started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop/{strategy_id}")
async def stop_strategy(strategy_id: str) -> Dict[str, str]:
    """Stop running strategy"""
    try:
        runtime = StrategyRuntime()
        await runtime.stop_strategy(strategy_id)
        
        return {
            "strategy_id": strategy_id,
            "status": "stopped"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Strategy not found")


@router.get("/{strategy_id}/status")
async def get_strategy_status(strategy_id: str) -> StrategyResponse:
    """Get strategy execution status"""
    # TODO: Implement database lookup
    return StrategyResponse(
        id=strategy_id,
        status="running",
        symbol="BTCUSDT",
        pnl=125.50,
        trades_count=8,
        uptime_seconds=3600
    )