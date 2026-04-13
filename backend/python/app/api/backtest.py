from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.backtest.engine import BacktestEngine
from app.services.backtest.report import BacktestReportService
from app.schemas.backtest import BacktestRequest, BacktestResponse

router = APIRouter()


@router.post("/run")
async def run_backtest(request: BacktestRequest) -> Dict[str, Any]:
    """Run a backtest"""
    try:
        engine = BacktestEngine()
        result = await engine.run_backtest(
            strategy_code=request.strategy_code,
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital
        )
        
        return {
            "backtest_id": result.id,
            "status": "completed",
            "summary": result.summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{backtest_id}")
async def get_backtest_result(backtest_id: str) -> BacktestResponse:
    """Get backtest result"""
    # TODO: Implement database lookup
    return BacktestResponse(
        id=backtest_id,
        status="completed",
        total_return=15.5,
        sharpe_ratio=1.2,
        max_drawdown=8.3,
        trades_count=45
    )


@router.get("/{backtest_id}/report")
async def get_backtest_report(backtest_id: str) -> Dict[str, Any]:
    """Get detailed backtest report"""
    report_service = BacktestReportService()
    report = await report_service.generate_report(backtest_id)
    
    return {
        "backtest_id": backtest_id,
        "report": report,
        "charts": ["equity_curve", "drawdown", "returns_distribution"]
    }