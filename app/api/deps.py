from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.database.session import get_db
from app.models.entities import User
from app.models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inválido")
    return user


def require_roles(*roles: UserRole):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles and current_user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Permissão insuficiente")
        return current_user
    return checker
