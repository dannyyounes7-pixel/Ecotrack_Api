from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdateAdmin
from app.core.config import get_current_user, require_admin

router = APIRouter()


# ✅ Route utile : récupérer son profil (user ou admin)
@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ Liste paginée des users (ADMIN)
@router.get("/", response_model=list[UserOut])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# ✅ Récupérer un user par id (ADMIN)
@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user_admin(
    user_id: int,
    payload: UserUpdateAdmin,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if payload.role is not None:
        if payload.role not in ["user", "admin"]:
            raise HTTPException(status_code=400, detail="Rôle invalide")
        user.role = payload.role

    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    db.delete(user)
    db.commit()
    return None
