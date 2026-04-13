from typing import Dict, List, Any
from datetime import datetime, timedelta
from app.services.ai.analysis_memory import AnalysisMemoryService


class AICalibrationService:
    def __init__(self):
        self.memory = AnalysisMemoryService()
    
    async def calibrate_confidence(self, symbol: str, analysis: Dict[str, Any]) -> float:
        """Calibrate confidence score based on historical accuracy"""
        
        accuracy_metrics = await self.memory.get_accuracy_metrics(symbol)
        base_confidence = analysis.get("confidence", 0.5)
        
        # Adjust confidence based on historical accuracy
        historical_accuracy = accuracy_metrics.get("accuracy", 0.5)
        verification_count = accuracy_metrics.get("verified_analyses", 0)
        
        # Confidence adjustment factor
        if verification_count > 10:
            # Enough data for calibration
            adjustment = (historical_accuracy - 0.5) * 0.3  # Scale adjustment
            calibrated_confidence = base_confidence + adjustment
        elif verification_count > 5:
            # Some data, smaller adjustment
            adjustment = (historical_accuracy - 0.5) * 0.15
            calibrated_confidence = base_confidence + adjustment
        else:
            # Insufficient data, slight conservative bias
            calibrated_confidence = base_confidence * 0.9
        
        # Keep confidence within bounds
        calibrated_confidence = max(0.1, min(0.95, calibrated_confidence))
        
        return calibrated_confidence
    
    async def get_model_performance_stats(self, days_back: int = 30) -> Dict[str, Any]:
        """Get performance statistics for the AI model"""
        
        # This would typically query a database of all analyses
        # For now, return sample stats
        return {
            "total_analyses": 145,
            "verified_predictions": 98,
            "overall_accuracy": 0.67,
            "accuracy_by_timeframe": {
                "1_day": 0.72,
                "1_week": 0.65,
                "1_month": 0.61
            },
            "accuracy_by_market_condition": {
                "bull_market": 0.71,
                "bear_market": 0.63,
                "sideways": 0.58
            },
            "confidence_calibration": {
                "high_confidence_accuracy": 0.78,
                "medium_confidence_accuracy": 0.65,
                "low_confidence_accuracy": 0.52
            },
            "bias_metrics": {
                "bullish_bias": 0.12,  # Tendency to predict up moves
                "overconfidence": 0.08  # Confidence vs actual accuracy gap
            }
        }
    
    async def suggest_model_improvements(self) -> List[str]:
        """Suggest improvements based on performance analysis"""
        stats = await self.get_model_performance_stats()
        
        suggestions = []
        
        if stats["overall_accuracy"] < 0.6:
            suggestions.append("Consider ensemble approach with multiple models")
        
        if stats["bias_metrics"]["bullish_bias"] > 0.15:
            suggestions.append("Address bullish bias in predictions")
        
        if stats["bias_metrics"]["overconfidence"] > 0.1:
            suggestions.append("Implement confidence score calibration")
        
        if stats["accuracy_by_market_condition"]["sideways"] < 0.55:
            suggestions.append("Improve sideways market detection")
        
        return suggestions or ["Current model performance is satisfactory"]