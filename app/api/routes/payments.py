from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.entities import Order, Payment, RestaurantTable, User
from app.models.enums import PaymentStatus, TableStatus
from app.schemas import PaymentCreate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Pagamentos"])


@router.post("/", response_model=PaymentOut)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    order = db.get(Order, payload.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if payload.amount < order.total:
        raise HTTPException(status_code=400, detail="Valor menor que o total do pedido")

    payment = Payment(**payload.model_dump())
    order.payment_status = PaymentStatus.paid

    table = db.get(RestaurantTable, order.table_id)
    if table:
        table.status = TableStatus.closed
        table.people_count = 0

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
