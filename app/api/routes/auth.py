from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, hash_password
from app.database.session import get_db
from app.models.entities import User
from app.schemas import Login, Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return Token(access_token=create_access_token(user.email))
