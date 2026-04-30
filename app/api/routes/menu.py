from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.entities import Category, MenuItem, User
from app.schemas import CategoryCreate, CategoryOut, MenuItemCreate, MenuItemOut

router = APIRouter(prefix="/menu", tags=["Cardápio"])


@router.post("/categories", response_model=CategoryOut)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()


@router.post("/items", response_model=MenuItemOut)
def create_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not db.get(Category, payload.category_id):
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    item = MenuItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items", response_model=list[MenuItemOut])
def list_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).filter(MenuItem.is_available == True).order_by(MenuItem.name).all()
