from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.entities import MenuItem, Order, OrderItem, RestaurantTable, StockItem, User
from app.models.enums import OrderStatus, TableStatus
from app.schemas import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.post("/", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    table = db.get(RestaurantTable, payload.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if not payload.items:
        raise HTTPException(status_code=400, detail="Pedido precisa ter pelo menos um item")

    order = Order(
        table_id=payload.table_id,
        waiter_id=user.id,
        notes=payload.notes,
        preparation_time_minutes=payload.preparation_time_minutes,
        status=OrderStatus.sent,
    )
    db.add(order)
    db.flush()

    total = 0.0
    for item_payload in payload.items:
        menu_item = db.get(MenuItem, item_payload.menu_item_id)
        if not menu_item or not menu_item.is_available:
            raise HTTPException(status_code=404, detail=f"Item {item_payload.menu_item_id} indisponível")

        stock = db.query(StockItem).filter(StockItem.menu_item_id == menu_item.id).first()
        if stock:
            if stock.current_quantity < item_payload.quantity:
                raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {menu_item.name}")
            stock.current_quantity -= item_payload.quantity

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_payload.quantity,
            unit_price=menu_item.price,
            notes=item_payload.notes,
            status=OrderStatus.sent,
        )
        total += menu_item.price * item_payload.quantity
        db.add(order_item)

    order.total = total
    table.status = TableStatus.occupied
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Order).order_by(Order.id.desc()).all()


@router.get("/sector/{sector}", response_model=list[OrderOut])
def list_orders_by_sector(sector: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    orders = db.query(Order).join(OrderItem).join(MenuItem).filter(MenuItem.sector == sector).distinct().all()
    return orders


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    order.status = payload.status
    if payload.preparation_time_minutes is not None:
        order.preparation_time_minutes = payload.preparation_time_minutes
    for item in order.items:
        item.status = payload.status
    db.commit()
    db.refresh(order)
    return order
