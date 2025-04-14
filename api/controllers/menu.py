from sqlalchemy.orm import Session
from ..models.menu import menu
from ..schemas.menu import menuSchema

def create_menu_item(db: Session, request: menuSchema):
    new_item = menu(**request.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_all_menu_items(db: Session):
    return db.query(menu).all()

def get_menu_item_by_id(db: Session, item_id: int):
    return db.query(menu).filter(menu.dish_id == item_id).first()

def update_menu_item(db: Session, item_id: int, request: menuSchema):
    item = db.query(menu).filter(menu.dish_id == item_id).first()
    if item:
        for key, value in request.dict().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_menu_item(db: Session, item_id: int):
    item = db.query(menu).filter(menu.dish_id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item