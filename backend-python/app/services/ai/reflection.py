from typing import Dict, Any
from app.services.ai.llm_service import LLMService


class ReflectionService:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def reflect_on_analysis(self, original_analysis: str, symbol: str) -> Dict[str, Any]:
        """Perform reflection loop to improve analysis quality"""
        
        reflection_prompt = f"""
        Review and critique this analysis of {symbol}:
        
        ORIGINAL ANALYSIS:
        {original_analysis}
        
        As an expert analyst, identify:
        1. Strengths in this analysis
        2. Potential weaknesses or biases
        3. Missing considerations
        4. Areas that need more evidence
        5. Confidence level assessment
        
        Then provide an IMPROVED analysis addressing these issues.
        """
        
        reflection = await self.llm_service.analyze(symbol, reflection_prompt)
        
        # Extract improvement suggestions
        improvement_prompt = f"""
        Based on this reflection:
        {reflection}
        
        Provide a FINAL IMPROVED analysis of {symbol} that addresses the identified weaknesses.
        """
        
        improved_analysis = await self.llm_service.analyze(symbol, improvement_prompt)
        
        return {
            "original_analysis": original_analysis,
            "reflection": reflection,
            "improved_analysis": improved_analysis,
            "improvement_score": self._calculate_improvement_score(original_analysis, improved_analysis)
        }
    
    def _calculate_improvement_score(self, original: str, improved: str) -> float:
        """Calculate how much the analysis improved"""
        # Simple heuristic based on length and detail
        length_improvement = len(improved) / len(original) if original else 1.0
        return min(1.0, length_improvement * 0.8 + 0.2)  # Cap at 1.0