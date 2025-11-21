from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate, SourceOut
from app.core.config import require_admin, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SourceOut, status_code=201)
def create_source(payload: SourceCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing = db.query(Source).filter(Source.name == payload.name).first()
    if existing:
        raise HTTPException(400, "Source déjà existante")
    source = Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source

@router.get("/", response_model=list[SourceOut])
def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
    __: User = Depends(get_current_user),
):
    q = db.query(Source)
    if search:
        q = q.filter(Source.name.ilike(f"%{search}%"))
    return q.offset(skip).limit(limit).all()

@router.get("/{source_id}", response_model=SourceOut)
def get_source(source_id: int, db: Session = Depends(get_db), __: User = Depends(get_current_user)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(404, "Source introuvable")
    return source

@router.patch("/{source_id}", response_model=SourceOut)
def update_source(source_id: int, payload: SourceUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(404, "Source introuvable")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(source, k, v)

    db.commit()
    db.refresh(source)
    return source

@router.delete("/{source_id}", status_code=204)
def delete_source(source_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(404, "Source introuvable")
    db.delete(source)
    db.commit()
    return None
