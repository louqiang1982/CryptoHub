from typing import AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.DEFAULT_LLM_MODEL,
            streaming=True
        )
    
    async def stream_analysis(self, symbol: str, prompt: str) -> AsyncGenerator[str, None]:
        """Stream AI analysis for given symbol and prompt"""
        full_prompt = f"""
        Analyze the cryptocurrency {symbol} based on the following request:
        {prompt}
        
        Provide a comprehensive analysis including:
        1. Technical analysis
        2. Market sentiment
        3. Risk assessment
        4. Trading recommendation
        """
        
        messages = [HumanMessage(content=full_prompt)]
        
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content'):
                yield chunk.content
    
    async def analyze(self, symbol: str, prompt: str) -> str:
        """Get complete analysis"""
        full_prompt = f"""
        Analyze {symbol}: {prompt}
        
        Provide structured analysis with clear recommendations.
        """
        
        messages = [HumanMessage(content=full_prompt)]
        response = await self.llm.ainvoke(messages)
        return response.content