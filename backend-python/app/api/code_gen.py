from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.ai.code_generator import CodeGeneratorService
from app.schemas.common import CodeGenRequest

router = APIRouter()


@router.post("/generate")
async def generate_strategy_code(request: CodeGenRequest) -> Dict[str, Any]:
    """Generate strategy code from natural language description"""
    try:
        generator = CodeGeneratorService()
        result = await generator.generate_strategy(
            description=request.description,
            strategy_type=request.strategy_type,
            complexity=request.complexity or "medium"
        )
        
        return {
            "generated_code": result.code,
            "explanation": result.explanation,
            "estimated_complexity": result.complexity,
            "suggested_parameters": result.parameters,
            "warnings": result.warnings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))