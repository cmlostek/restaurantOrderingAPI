from fastapi import HTTPException
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
    existing = db.query(menu).filter(menu.dish_id == request.dish_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Dish with this ID already exists.")

    ingredient_objs = db.query(resources).filter(resources.resource_id.in_(request.ingredients)).all()

    if len(ingredient_objs) != len(request.ingredients):
        raise HTTPException(status_code=400, detail="Some ingredient IDs are invalid.")

    new_item = menu(
        dish_id=request.dish_id,
        dish=request.dish,
        price=request.price,
        calories=request.calories,
        category=request.category
    )
    db.add(new_item)
    db.commit()

    db.refresh(new_item)
    new_item.ingredients = ingredient_objs
    db.commit()
    db.refresh(new_item)

    return {
        "dish_id": new_item.dish_id,
        "dish": new_item.dish,
        "price": float(new_item.price),
        "calories": new_item.calories,
        "category": new_item.category,
        "ingredients": [r.resource_id for r in new_item.ingredients]
    }

def get_all_menu_items(db: Session):
    return db.query(menu).all()

def get_menu_item_by_id(db: Session, item_id: int):
    return db.query(menu).filter(menu.dish_id == item_id).first()

def update_menu_item(db: Session, item_id: int, request: menuSchema):
    item = db.query(menu).filter(menu.dish_id == item_id).first()

    if item:
        data = request.dict()
        ingredient_ids = data.pop("ingredients", None)

        # Update all basic fields
        for key, value in data.items():
            setattr(item, key, value)

        # Safely update ingredients
        if ingredient_ids is not None:
            # Clear existing relationships
            item.ingredients = []
            db.commit()  # Important to commit the unlinking before re-linking

            # Fetch new ingredient objects
            ingredient_objs = db.query(resources).filter(resources.resource_id.in_(ingredient_ids)).all()

            if len(ingredient_objs) != len(set(ingredient_ids)):
                raise HTTPException(status_code=400, detail="Some ingredient IDs are invalid.")

            item.ingredients = ingredient_objs

        db.commit()
        db.refresh(item)

        return {
            "dish_id": item.dish_id,
            "dish": item.dish,
            "price": float(item.price),
            "calories": item.calories,
            "category": item.category,
            "ingredients": [r.resource_id for r in item.ingredients]
        }

    raise HTTPException(status_code=404, detail="Menu item not found.")

def delete_menu_item(db: Session, item_id: int):
    item = db.query(menu).filter(menu.dish_id == item_id).first()

    if item:
        response_data = {
            "dish_id": item.dish_id,
            "dish": item.dish,
            "price": float(item.price),
            "calories": item.calories,
            "category": item.category,
            "ingredients": [r.resource_id for r in item.ingredients]
        }
        db.delete(item)
        db.commit()
        return response_data

    raise HTTPException(status_code=404, detail="Menu item not found")

def search_menu_items(db: Session, keyword: str):
    items = db.query(menu).filter(menu.dish.ilike(f"%{keyword}%")).all()
    if not items:
        raise HTTPException(status_code=404, detail="No menu items found.")
    return items

def get_menu_items_by_category(db: Session, category: str):
    items = db.query(menu).filter(menu.category == category).all()
    if not items:
        raise HTTPException(status_code=404, detail="No menu items found in this category.")
    return items