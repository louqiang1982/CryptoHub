from typing import List, Dict, Any
from app.services.ai.llm_service import LLMService


class EnsembleService:
    def __init__(self):
        self.models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-3.5-turbo"
        ]
    
    async def consensus_analysis(self, symbol: str, prompt: str) -> Dict[str, Any]:
        """Get consensus analysis from multiple models"""
        
        results = []
        
        for model in self.models:
            llm_service = LLMService()
            # Override model for this instance
            llm_service.llm.model = model
            
            try:
                analysis = await llm_service.analyze(symbol, prompt)
                results.append({
                    "model": model,
                    "analysis": analysis,
                    "weight": self._get_model_weight(model)
                })
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
        
        return self._compute_consensus(results)
    
    def _get_model_weight(self, model: str) -> float:
        """Get weight for each model in consensus"""
        weights = {
            "gpt-4o": 0.5,
            "gpt-4o-mini": 0.3,
            "gpt-3.5-turbo": 0.2
        }
        return weights.get(model, 0.1)
    
    def _compute_consensus(self, results: List[Dict]) -> Dict[str, Any]:
        """Compute weighted consensus from model results"""
        if not results:
            return {"error": "No valid model responses"}
        
        # Simple consensus logic - can be enhanced
        consensus_score = sum(
            result["weight"] * 7.0  # Default score
            for result in results
        )
        
        return {
            "consensus_score": consensus_score,
            "model_count": len(results),
            "individual_results": results,
            "confidence": min(0.9, len(results) / len(self.models))
        }