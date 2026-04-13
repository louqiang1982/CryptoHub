from typing import Dict, Any
from app.services.ai.llm_service import LLMService


class CodeGeneratorService:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def generate_strategy(
        self, 
        description: str, 
        strategy_type: str = "technical", 
        complexity: str = "medium"
    ) -> 'CodeGenerationResult':
        """Generate trading strategy code from natural language description"""
        
        prompt = f"""
        Generate a Python trading strategy based on this description:
        
        DESCRIPTION: {description}
        TYPE: {strategy_type}
        COMPLEXITY: {complexity}
        
        Requirements:
        1. Use the following strategy template structure
        2. Implement proper risk management
        3. Include clear entry/exit logic
        4. Add appropriate comments
        5. Use pandas for data handling
        
        Template:
        ```python
        import pandas as pd
        import numpy as np
        from typing import Dict, Any, Optional
        
        class GeneratedStrategy:
            def __init__(self, parameters: Dict[str, Any]):
                self.parameters = parameters
                self.position = 0
                self.cash = parameters.get('initial_capital', 10000)
                
            def on_bar(self, bar: Dict[str, float]) -> Optional[Dict[str, Any]]:
                \"\"\"Process each price bar and return trading signal\"\"\"
                # Implement strategy logic here
                pass
                
            def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
                \"\"\"Calculate technical indicators\"\"\"
                # Implement indicator calculations
                return df
                
            def get_signal(self, df: pd.DataFrame, index: int) -> str:
                \"\"\"Get trading signal: 'BUY', 'SELL', or 'HOLD'\"\"\"
                # Implement signal logic
                return 'HOLD'
        ```
        
        Generate complete, executable Python code with explanation.
        """
        
        response = await self.llm_service.analyze("strategy", prompt)
        
        return CodeGenerationResult(
            code=self._extract_code(response),
            explanation=response,
            complexity=complexity,
            parameters=self._extract_parameters(response),
            warnings=self._get_warnings(response)
        )
    
    def _extract_code(self, response: str) -> str:
        """Extract Python code from LLM response"""
        # Find code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip() if end != -1 else response
        return response
    
    def _extract_parameters(self, response: str) -> Dict[str, Any]:
        """Extract suggested parameters"""
        return {
            "initial_capital": 10000,
            "risk_per_trade": 0.02,
            "max_positions": 1
        }
    
    def _get_warnings(self, response: str) -> list[str]:
        """Generate warnings for the strategy"""
        return [
            "Test thoroughly before live trading",
            "Adjust parameters based on market conditions",
            "Monitor performance regularly"
        ]


class CodeGenerationResult:
    def __init__(self, code: str, explanation: str, complexity: str, parameters: Dict, warnings: list):
        self.code = code
        self.explanation = explanation
        self.complexity = complexity
        self.parameters = parameters
        self.warnings = warnings