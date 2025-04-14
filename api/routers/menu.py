from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers.menu import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item_by_id,
    update_menu_item,
    delete_menu_item,
)
from ..schemas.menu import menuSchema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

@router.post("/", response_model=menuSchema)
def create_new_menu_item(request: menuSchema, db: Session = Depends(get_db)):
    return create_menu_item(db, request)

@router.get("/", response_model=list[menuSchema])
def read_all_menu_items(db: Session = Depends(get_db)):
    return get_all_menu_items(db)

@router.get("/{item_id}", response_model=menuSchema)
def read_menu_item_by_id(item_id: int, db: Session = Depends(get_db)):
    item = get_menu_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=menuSchema)
def update_existing_menu_item(item_id: int, request: menuSchema, db: Session = Depends(get_db)):
    item = update_menu_item(db, item_id, request)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.delete("/{item_id}", response_model=menuSchema)
def delete_existing_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = delete_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item