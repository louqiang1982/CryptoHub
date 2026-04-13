from fastapi import APIRouter
from typing import List, Dict, Any

from app.services.research.polymarket import PolymarketService

router = APIRouter()


@router.get("/markets")
async def list_polymarket_markets() -> List[Dict[str, Any]]:
    """List prediction markets from Polymarket"""
    service = PolymarketService()
    markets = await service.get_markets()
    
    return [
        {
            "id": market.id,
            "title": market.title,
            "description": market.description,
            "volume": market.volume,
            "liquidity": market.liquidity,
            "end_date": market.end_date.isoformat() if market.end_date else None,
            "outcomes": [
                {
                    "name": outcome.name,
                    "price": outcome.price,
                    "probability": outcome.probability
                }
                for outcome in market.outcomes
            ]
        }
        for market in markets
    ]