"""AI Analysis Pydantic schemas."""

from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    symbol: str
    analysis_type: str = "comprehensive"
    timeframe: str = "1D"
    include_technical: bool = True
    include_fundamental: bool = True
    include_sentiment: bool = True


class FastAnalysisRequest(BaseModel):
    symbol: str
    timeframe: str = "1H"


class AnalysisResponse(BaseModel):
    id: str
    symbol: str
    signal: str
    confidence: float
    summary: str | None
    technical_analysis: dict | None
    fundamental_analysis: dict | None
    sentiment_analysis: dict | None
    recommendation: str | None
    status: str

    model_config = {"from_attributes": True}
