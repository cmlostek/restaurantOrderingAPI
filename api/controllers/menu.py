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
    # Fetch resources based on the provided resource IDs
    ingredient_objs = db.query(resources).filter(resources.resource_id.in_(request.ingredients)).all()
    if len(ingredient_objs) != len(request.ingredients):
        raise ValueError("Some resource IDs are invalid")
    # Create the menu item with the fetched resources
    new_item = menu(
        dish=request.dish,
        price=request.price,
        calories=request.calories,
        category=request.category
    )
    new_item.ingredients =ingredient_objs  # Populate the relationship
    print("New item created:", new_item)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {
        "dish_id": new_item.dish_id,
        "dish": new_item.dish,
        "price": float(new_item.price),
        "calories": new_item.calories,
        "category": new_item.category,
        "ingredients": [r.resource_id for r in new_item.ingredients]  # THIS is the key fix
    }

def get_all_menu_items(db: Session):
    return db.query(menu).all()

def get_menu_item_by_id(db: Session, item_id: int):
    return db.query(menu).filter(menu.dish_id == item_id).first()

def update_menu_item(db: Session, item_id: int, request: menuSchema):
    item = db.query(menu).filter(menu.dish_id == item_id).first()

    if item:
        data = request.dict()
        # Extract ingredients from the request
        ingredients_ids = data.pop("ingredients", None)

        # Update the item with the rest of the data
        for key, value in data.items():
            setattr(item, key, value)

        if ingredients_ids is not None:
            # Fetch corresponding resource objects
            resource_objs = db.query(resources).filter(resources.resource_id.in_(ingredients_ids)).all()
            # Check if all resource IDs are valid
            if len(resource_objs) != len(ingredients_ids):
                raise ValueError("Some ingredient IDs are invalid")
            # Update the ingredient relationship
            item.ingredients = resource_objs
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