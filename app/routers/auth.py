from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user",
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Utilisateur créé avec succès"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )

    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
