from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base
from app.models.enums import UserRole, TableStatus, ItemSector, OrderStatus, PaymentStatus


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.waiter)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, default=4)
    people_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[TableStatus] = mapped_column(Enum(TableStatus), default=TableStatus.available)

    orders = relationship("Order", back_populates="table")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sector: Mapped[ItemSector] = mapped_column(Enum(ItemSector), default=ItemSector.kitchen)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="menu_items")
    stock = relationship("StockItem", back_populates="menu_item", uselist=False)


class StockItem(Base):
    __tablename__ = "stock_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), unique=True, nullable=False)
    current_quantity: Mapped[float] = mapped_column(Float, default=0)
    minimum_quantity: Mapped[float] = mapped_column(Float, default=5)
    unit: Mapped[str] = mapped_column(String(20), default="un")

    menu_item = relationship("MenuItem", back_populates="stock")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("restaurant_tables.id"), nullable=False)
    waiter_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.opened)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.pending)
    preparation_time_minutes: Mapped[int] = mapped_column(Integer, default=20)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    total: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    table = relationship("RestaurantTable", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.sent)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    method: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
