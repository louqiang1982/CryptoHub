from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
from typing import Dict, Any

from app.services.ai.llm_service import LLMService
from app.services.ai.fast_analysis import FastAnalysisService
from app.schemas.analysis import AnalysisRequest, AnalysisResponse

router = APIRouter()


@router.post("/analyze")
async def stream_ai_analysis(request: AnalysisRequest):
    """Stream AI analysis results using SSE"""
    
    async def generate():
        try:
            llm_service = LLMService()
            async for chunk in llm_service.stream_analysis(request.symbol, request.prompt):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield f"data: {json.dumps({'status': 'complete'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.get("/analyze/{analysis_id}")
async def get_analysis_result(analysis_id: str) -> AnalysisResponse:
    """Get completed analysis result"""
    # TODO: Implement database lookup
    return AnalysisResponse(
        id=analysis_id,
        status="completed",
        result="Sample analysis result",
        confidence=0.85
    )


@router.post("/fast-analyze")
async def fast_analyze(request: AnalysisRequest) -> Dict[str, Any]:
    """Quick multi-factor analysis"""
    fast_analysis = FastAnalysisService()
    result = await fast_analysis.analyze_multi_factor(request.symbol)
    
    return {
        "symbol": request.symbol,
        "analysis": result,
        "timestamp": "2024-01-01T00:00:00Z"
    }