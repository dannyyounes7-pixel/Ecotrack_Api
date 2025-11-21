from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate, ZoneOut
from app.core.config import require_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ZoneOut, status_code=201)
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    zone = Zone(**payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone

@router.get("/", response_model=list[ZoneOut])
def list_zones(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),
):
    q = db.query(Zone)
    if search:
        q = q.filter(Zone.name.ilike(f"%{search}%"))
    return q.offset(skip).limit(limit).all()

@router.get("/{zone_id}", response_model=ZoneOut)
def get_zone(zone_id: int, db: Session = Depends(get_db), __: User = Depends(get_current_user)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(404, "Zone introuvable")
    return zone

@router.patch("/{zone_id}", response_model=ZoneOut)
def update_zone(zone_id: int, payload: ZoneUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(404, "Zone introuvable")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(zone, k, v)

    db.commit()
    db.refresh(zone)
    return zone

@router.delete("/{zone_id}", status_code=204)
def delete_zone(zone_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(404, "Zone introuvable")
    db.delete(zone)
    db.commit()
    return None
