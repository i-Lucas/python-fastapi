from database import get_db
from fastapi import APIRouter, Depends
from models import MVP_Table, ItemCreate

database_mvp_router = APIRouter(prefix="")

@database_mvp_router.post("/database/mvp")
def create_item(item: ItemCreate, db = Depends(get_db)):

    new_item = MVP_Table(name=item.name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return 201

@database_mvp_router.get("/database/mvp")
def get_items(db = Depends(get_db)):
    items = db.query(MVP_Table).all()
    return items