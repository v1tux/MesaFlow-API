from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.database.session import get_db
from app.models.entities import MenuItem, StockItem, User
from app.models.enums import UserRole
from app.schemas import StockCreate, StockOut

router = APIRouter(prefix="/stock", tags=["Estoque"])


def serialize(stock: StockItem) -> dict:
    return {
        "id": stock.id,
        "menu_item_id": stock.menu_item_id,
        "current_quantity": stock.current_quantity,
        "minimum_quantity": stock.minimum_quantity,
        "unit": stock.unit,
        "low_stock": stock.current_quantity <= stock.minimum_quantity,
    }


@router.post("/", response_model=StockOut)
def create_stock(payload: StockCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.manager))):
    if not db.get(MenuItem, payload.menu_item_id):
        raise HTTPException(status_code=404, detail="Item do cardápio não encontrado")
    stock = StockItem(**payload.model_dump())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return serialize(stock)


@router.get("/", response_model=list[StockOut])
def list_stock(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.manager))):
    return [serialize(s) for s in db.query(StockItem).all()]


@router.get("/alerts", response_model=list[StockOut])
def low_stock_alerts(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.manager))):
    stocks = db.query(StockItem).filter(StockItem.current_quantity <= StockItem.minimum_quantity).all()
    return [serialize(s) for s in stocks]
