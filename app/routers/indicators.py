from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import datetime

from app.database import get_db
from app.models.indicator import Indicator
from app.models.zone import Zone
from app.models.source import Source
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate, IndicatorOut
from app.core.config import require_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=IndicatorOut, status_code=201)
def create_indicator(payload: IndicatorCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not db.query(Zone).filter(Zone.id == payload.zone_id).first():
        raise HTTPException(404, "Zone introuvable")
    if not db.query(Source).filter(Source.id == payload.source_id).first():
        raise HTTPException(404, "Source introuvable")

    data = payload.model_dump()
    metadata = data.pop("metadata", None)
    indic = Indicator(**data, metadata_=metadata)

    db.add(indic)
    db.commit()
    db.refresh(indic)
    return indic

@router.get("/", response_model=list[IndicatorOut])
def list_indicators(
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),

    from_date: datetime | None = Query(None),
    to_date: datetime | None = Query(None),
    zone_id: int | None = None,
    source_id: int | None = None,
    type: str | None = None,

    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("desc", pattern="^(asc|desc)$"),
):
    q = db.query(Indicator)

    if from_date:
        q = q.filter(Indicator.timestamp >= from_date)
    if to_date:
        q = q.filter(Indicator.timestamp <= to_date)
    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)
    if source_id:
        q = q.filter(Indicator.source_id == source_id)
    if type:
        q = q.filter(Indicator.type == type)

    q = q.order_by(desc(Indicator.timestamp) if sort == "desc" else asc(Indicator.timestamp))

    return q.offset(skip).limit(limit).all()

@router.get("/{indicator_id}", response_model=IndicatorOut)
def get_indicator(indicator_id: int, db: Session = Depends(get_db), __: User = Depends(get_current_user)):
    indic = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not indic:
        raise HTTPException(404, "Indicateur introuvable")
    return indic

@router.patch("/{indicator_id}", response_model=IndicatorOut)
def update_indicator(indicator_id: int, payload: IndicatorUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    indic = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not indic:
        raise HTTPException(404, "Indicateur introuvable")

    data = payload.model_dump(exclude_unset=True)
    if "metadata" in data:
        indic.metadata_ = data.pop("metadata")

    for k, v in data.items():
        setattr(indic, k, v)

    db.commit()
    db.refresh(indic)
    return indic

@router.delete("/{indicator_id}", status_code=204)
def delete_indicator(indicator_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    indic = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not indic:
        raise HTTPException(404, "Indicateur introuvable")
    db.delete(indic)
    db.commit()
    return None
