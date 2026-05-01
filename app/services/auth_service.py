from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token

class AuthService:

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = AuthService.authenticate_user(db, email, password)

        if not user:
            return None

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }