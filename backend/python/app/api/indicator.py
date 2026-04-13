from fastapi import APIRouter
from typing import Dict, Any, List

from app.services.strategy.indicator_strategy import IndicatorCalculator
from app.schemas.common import IndicatorRequest

router = APIRouter()


@router.post("/calculate")
async def calculate_indicators(request: IndicatorRequest) -> Dict[str, Any]:
    """Calculate technical indicators"""
    calculator = IndicatorCalculator()
    
    results = {}
    for indicator in request.indicators:
        result = await calculator.calculate(
            symbol=request.symbol,
            indicator_type=indicator.type,
            period=indicator.period,
            params=indicator.params or {}
        )
        results[indicator.type] = result
    
    return {
        "symbol": request.symbol,
        "indicators": results,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/list")
async def list_available_indicators() -> List[Dict[str, Any]]:
    """List all available technical indicators"""
    return [
        {
            "name": "SMA",
            "description": "Simple Moving Average",
            "parameters": ["period"]
        },
        {
            "name": "EMA",
            "description": "Exponential Moving Average", 
            "parameters": ["period"]
        },
        {
            "name": "RSI",
            "description": "Relative Strength Index",
            "parameters": ["period"]
        },
        {
            "name": "MACD",
            "description": "Moving Average Convergence Divergence",
            "parameters": ["fast_period", "slow_period", "signal_period"]
        },
        {
            "name": "BB",
            "description": "Bollinger Bands",
            "parameters": ["period", "std_dev"]
        }
    ]