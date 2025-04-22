from sqlalchemy.orm import Session
from ..models.menu import menu
from ..models.resources import resources
from ..schemas.menu import menuSchema

def serialize_menu(menu_obj):
    return {
        "dish_id": menu_obj.dish_id,
        "dish": menu_obj.dish,
        "price": float(menu_obj.price),
        "calories": menu_obj.calories,
        "category": menu_obj.category,
        "ingredients": [r.resource_id for r in menu_obj.ingredients]  # THIS is the key fix
    }

def create_menu_item(db: Session, request: menuSchema):
    # Fetch resources based on the provided resource IDs
    ingredient_objs = db.query(resources).filter(resources.resource_id.in_(request.ingredients)).all()

    if len(ingredient_objs) != len(request.ingredients):
        raise ValueError("Some resource IDs are invalid")

    # Create the menu item with the fetched resources
    new_item = menu(
        dish=request.dish,
        price=request.price,
        ingredients=ingredient_objs,  # Populate the relationship
        calories=request.calories,
        category=request.category
    )
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