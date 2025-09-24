from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from ...models.item import Item
from ...schemas.item import AnalyzeIn, ItemOut, StatsOut
from ...services.sentiment import score_text
from ...api.deps import db_dep

router = APIRouter(prefix="/items", tags=["items"])

@router.post("", response_model=ItemOut)
def analyze(payload: AnalyzeIn, db: Session = Depends(db_dep)):
    label, compound = score_text(payload.text)
    row = Item(text=payload.text, sentiment_label=label, sentiment_score=compound)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("", response_model=List[ItemOut])
def list_items(
    db: Session = Depends(db_dep),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    q: Optional[str] = None,
    label: Optional[str] = Query(None, pattern="^(pos|neu|neg)$"),
):
    qry = db.query(Item)
    if q:
        like = f"%{q}%"
        qry = qry.filter(Item.text.like(like))
    if label:
        qry = qry.filter(Item.sentiment_label == label)
    return qry.order_by(Item.id.desc()).offset(offset).limit(limit).all()

@router.get("/stats", response_model=StatsOut)
def stats(db: Session = Depends(db_dep)):
    total = db.query(func.count(Item.id)).scalar() or 0
    pos, neu, neg, avg = (
        db.query(
            func.sum(case((Item.sentiment_label == "pos", 1), else_=0)),
            func.sum(case((Item.sentiment_label == "neu", 1), else_=0)),
            func.sum(case((Item.sentiment_label == "neg", 1), else_=0)),
            func.avg(Item.sentiment_score),
        ).one()
    )
    return {
        "total": total,
        "pos": int(pos or 0),
        "neu": int(neu or 0),
        "neg": int(neg or 0),
        "avg_compound": float(avg or 0.0),
    }
