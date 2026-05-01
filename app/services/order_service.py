from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate

class OrderService:

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate):
        new_order = Order(
            table_id=order_data.table_id,
            description=order_data.description,
            status="pending"
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order

    @staticmethod
    def update_status(db: Session, order_id: int, status: str):
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            return None

        order.status = status
        db.commit()
        db.refresh(order)

        return order
