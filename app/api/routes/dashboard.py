from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.database.session import get_db
from app.models.entities import Order, RestaurantTable, StockItem, User
from app.models.enums import PaymentStatus, TableStatus, UserRole
from app.schemas import DashboardOut

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.manager))):
    total_orders = db.query(Order).count()
    paid_orders = db.query(Order).filter(Order.payment_status == PaymentStatus.paid).count()
    revenue = db.query(func.coalesce(func.sum(Order.total), 0)).filter(Order.payment_status == PaymentStatus.paid).scalar() or 0
    occupied_tables = db.query(RestaurantTable).filter(RestaurantTable.status == TableStatus.occupied).count()
    low_stock_items = db.query(StockItem).filter(StockItem.current_quantity <= StockItem.minimum_quantity).count()
    average_ticket = revenue / paid_orders if paid_orders else 0

    return DashboardOut(
        total_orders=total_orders,
        paid_orders=paid_orders,
        revenue=round(revenue, 2),
        average_ticket=round(average_ticket, 2),
        occupied_tables=occupied_tables,
        low_stock_items=low_stock_items,
    )
