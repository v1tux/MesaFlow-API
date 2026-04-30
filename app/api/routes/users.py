from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.database.session import get_db
from app.models.entities import User
from app.models.enums import UserRole
from app.schemas import UserOut

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.manager))):
    return db.query(User).order_by(User.id.desc()).all()
