from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.entities import RestaurantTable, User
from app.models.enums import TableStatus
from app.schemas import TableCreate, TableOut, TableUpdate

router = APIRouter(prefix="/tables", tags=["Mesas"])


@router.post("/", response_model=TableOut)
def create_table(payload: TableCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    table = RestaurantTable(number=payload.number, seats=payload.seats)
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.get("/", response_model=list[TableOut])
def list_tables(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(RestaurantTable).order_by(RestaurantTable.number).all()


@router.patch("/{table_id}", response_model=TableOut)
def update_table(table_id: int, payload: TableUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    table = db.get(RestaurantTable, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if payload.people_count is not None:
        table.people_count = payload.people_count
        table.status = TableStatus.occupied if payload.people_count > 0 else TableStatus.available
    if payload.status is not None:
        table.status = payload.status
    db.commit()
    db.refresh(table)
    return table
