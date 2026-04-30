from fastapi import FastAPI
from app.core.config import settings
from app.core.security import hash_password
from app.database.session import Base, engine, SessionLocal
from app.models.entities import User, Category, MenuItem, RestaurantTable, StockItem
from app.models.enums import UserRole, ItemSector
from app.api.routes import auth, users, tables, menu, stock, orders, payments, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema completo de pedidos para restaurante com garçons, cozinha, bar, estoque, pagamento e dashboard.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tables.router)
app.include_router(menu.router)
app.include_router(stock.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def seed_initial_data():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@mesaflow.com").first()
        if not admin:
            db.add(User(
                name="Administrador MesaFlow",
                email="admin@mesaflow.com",
                hashed_password=hash_password("admin123"),
                role=UserRole.admin,
            ))

        if db.query(RestaurantTable).count() == 0:
            for number in range(1, 11):
                db.add(RestaurantTable(number=number, seats=4))

        if db.query(Category).count() == 0:
            pratos = Category(name="Pratos", description="Refeições principais")
            bebidas = Category(name="Bebidas", description="Bebidas do bar")
            db.add_all([pratos, bebidas])
            db.flush()
            burger = MenuItem(
                name="Burger Artesanal",
                description="Hambúrguer artesanal com queijo e molho da casa",
                price=32.90,
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                sector=ItemSector.kitchen,
                category_id=pratos.id,
            )
            suco = MenuItem(
                name="Suco Natural",
                description="Suco natural da fruta",
                price=12.00,
                image_url="https://images.unsplash.com/photo-1622597467836-f3285f2131b8",
                sector=ItemSector.bar,
                category_id=bebidas.id,
            )
            db.add_all([burger, suco])
            db.flush()
            db.add_all([
                StockItem(menu_item_id=burger.id, current_quantity=50, minimum_quantity=10, unit="un"),
                StockItem(menu_item_id=suco.id, current_quantity=40, minimum_quantity=8, unit="un"),
            ])
        db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "MesaFlow API online",
        "docs": "/docs",
        "admin": "admin@mesaflow.com / admin123",
    }
