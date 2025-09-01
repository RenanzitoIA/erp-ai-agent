from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ERPEvent(BaseModel):
    event: str
    payload: Dict[str, Any]

class AskInput(BaseModel):
    question: str
    context: Optional[str] = None
    kpis: Optional[dict] = None

class ForecastRequest(BaseModel):
    series: List[float]
    horizon: int = 12
