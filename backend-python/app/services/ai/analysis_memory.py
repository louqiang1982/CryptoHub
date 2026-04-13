from typing import Dict, List, Any
from datetime import datetime
from app.core.redis import redis_manager
import json


class AnalysisMemoryService:
    def __init__(self):
        self.redis = redis_manager
    
    async def store_analysis(self, symbol: str, analysis: Dict[str, Any]) -> str:
        """Store analysis for future reference"""
        analysis_id = f"analysis:{symbol}:{datetime.utcnow().isoformat()}"
        
        analysis_data = {
            "symbol": symbol,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat(),
            "performance": None  # To be updated later
        }
        
        await self.redis.set(analysis_id, json.dumps(analysis_data), ex=86400 * 30)  # 30 days
        
        # Add to symbol index
        await self._add_to_symbol_index(symbol, analysis_id)
        
        return analysis_id
    
    async def get_historical_analyses(self, symbol: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get historical analyses for a symbol"""
        index_key = f"symbol_index:{symbol}"
        analysis_ids = await self.redis.get(index_key)
        
        if not analysis_ids:
            return []
        
        ids = json.loads(analysis_ids)[-limit:]
        analyses = []
        
        for aid in ids:
            data = await self.redis.get(aid)
            if data:
                analyses.append(json.loads(data))
        
        return analyses
    
    async def update_analysis_performance(self, analysis_id: str, actual_outcome: Dict[str, Any]):
        """Update analysis with actual market performance"""
        data = await self.redis.get(analysis_id)
        if data:
            analysis_data = json.loads(data)
            analysis_data["performance"] = actual_outcome
            await self.redis.set(analysis_id, json.dumps(analysis_data))
    
    async def get_accuracy_metrics(self, symbol: str) -> Dict[str, float]:
        """Calculate accuracy metrics for past analyses"""
        analyses = await self.get_historical_analyses(symbol, limit=50)
        
        if not analyses:
            return {"accuracy": 0.0, "total_analyses": 0}
        
        correct_predictions = sum(
            1 for analysis in analyses
            if analysis.get("performance") and self._was_prediction_correct(analysis)
        )
        
        total_with_performance = sum(
            1 for analysis in analyses
            if analysis.get("performance")
        )
        
        accuracy = correct_predictions / total_with_performance if total_with_performance > 0 else 0.0
        
        return {
            "accuracy": accuracy,
            "total_analyses": len(analyses),
            "verified_analyses": total_with_performance
        }
    
    async def _add_to_symbol_index(self, symbol: str, analysis_id: str):
        """Add analysis ID to symbol index"""
        index_key = f"symbol_index:{symbol}"
        existing = await self.redis.get(index_key)
        
        if existing:
            ids = json.loads(existing)
        else:
            ids = []
        
        ids.append(analysis_id)
        
        # Keep only last 100 analyses per symbol
        if len(ids) > 100:
            ids = ids[-100:]
        
        await self.redis.set(index_key, json.dumps(ids))
    
    def _was_prediction_correct(self, analysis: Dict[str, Any]) -> bool:
        """Check if prediction was correct based on actual performance"""
        # Simple heuristic - can be enhanced
        performance = analysis.get("performance", {})
        predicted_direction = analysis.get("analysis", {}).get("recommendation", "HOLD")
        actual_return = performance.get("return", 0.0)
        
        if predicted_direction == "BUY" and actual_return > 0.05:
            return True
        elif predicted_direction == "SELL" and actual_return < -0.05:
            return True
        elif predicted_direction == "HOLD" and abs(actual_return) < 0.05:
            return True
        
        return False