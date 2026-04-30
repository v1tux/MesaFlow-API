from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    waiter = "waiter"
    kitchen = "kitchen"
    bar = "bar"


class TableStatus(str, Enum):
    available = "available"
    occupied = "occupied"
    payment_pending = "payment_pending"
    closed = "closed"


class ItemSector(str, Enum):
    kitchen = "kitchen"
    bar = "bar"


class OrderStatus(str, Enum):
    opened = "opened"
    sent = "sent"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    canceled = "canceled"


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    canceled = "canceled"
