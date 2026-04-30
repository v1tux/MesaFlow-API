from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.enums import UserRole, TableStatus, ItemSector, OrderStatus, PaymentStatus


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole = UserRole.waiter


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class TableCreate(BaseModel):
    number: int
    seats: int = 4


class TableUpdate(BaseModel):
    people_count: int | None = None
    status: TableStatus | None = None


class TableOut(BaseModel):
    id: int
    number: int
    seats: int
    people_count: int
    status: TableStatus

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryOut(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None
    sector: ItemSector = ItemSector.kitchen
    category_id: int
    is_available: bool = True


class MenuItemOut(MenuItemCreate):
    id: int

    class Config:
        from_attributes = True


class StockCreate(BaseModel):
    menu_item_id: int
    current_quantity: float = 0
    minimum_quantity: float = 5
    unit: str = "un"


class StockOut(StockCreate):
    id: int
    low_stock: bool

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)
    notes: str | None = None


class OrderCreate(BaseModel):
    table_id: int
    notes: str | None = None
    preparation_time_minutes: int = 20
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    notes: str | None
    status: OrderStatus

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    table_id: int
    waiter_id: int | None
    status: OrderStatus
    payment_status: PaymentStatus
    preparation_time_minutes: int
    notes: str | None
    total: float
    created_at: datetime
    items: list[OrderItemOut] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    preparation_time_minutes: int | None = None


class PaymentCreate(BaseModel):
    order_id: int
    method: str = "pix"
    amount: float


class PaymentOut(BaseModel):
    id: int
    order_id: int
    method: str
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardOut(BaseModel):
    total_orders: int
    paid_orders: int
    revenue: float
    average_ticket: float
    occupied_tables: int
    low_stock_items: int
