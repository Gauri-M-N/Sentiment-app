from pydantic import BaseModel
from datetime import datetime
class AnalyzeIn(BaseModel):
    text: str

class ItemOut(BaseModel):
    id: int
    text: str
    sentiment_label: str
    sentiment_score: float
    created_at: datetime
    class Config:
        from_attributes = True  # Pydantic v2; use orm_mode=True on v1

class StatsOut(BaseModel):
    total: int
    pos: int
    neu: int
    neg: int
    avg_compound: float
