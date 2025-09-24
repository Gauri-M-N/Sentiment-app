from sqlalchemy import Column, Integer, String, Float, DateTime, func
from ..core.db import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment_label = Column(String, nullable=False)   # 'pos'|'neu'|'neg'
    sentiment_score = Column(Float, nullable=False)    # scalar for charts
    created_at = Column(DateTime, server_default=func.now())
