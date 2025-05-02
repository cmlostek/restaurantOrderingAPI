from datetime import datetime, time, date

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from ..models.orders import Order
from api.models import resources as res_model, menu as menu_model, orders as order_model
from ..schemas.orders import OrderSchema

def create_order(db: Session, request: OrderSchema):
    # 1) Fetch and validate the dish
    dish = db.query(menu_model.menu).get(request.dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # 2) Check & decrement each ingredient
    for ing in dish.ingredients:
        if ing.quantity_available < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{ing.resource_name}'"
            )
        ing.quantity_available -= 1

    db.commit()    # persist inventory changes

    new_order = order_model.Order(
        user_id     = request.user_id,
        dish_id     = request.dish_id,
        order_date  = request.order_date,
        total_price = request.total_price,
        is_guest    = request.is_guest,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()

def update_order(db: Session, order_id: int, request: OrderSchema):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        for key, value in request.dict().items():
            setattr(order, key, value)
        db.commit()
        db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order

def get_order_by_date(db: Session, order_date: str):
    return db.query(Order).filter(Order.order_date == order_date).all()

def filter_order_dates(db: Session, start_date: date, end_date: date):
    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)

    orders = (
        db.query(Order)
        .filter(and_(
            Order.order_date >= start_dt,
            Order.order_date <= end_dt
        ))
        .all()
    )
    if not orders:
        raise HTTPException(404, f"No orders between {start_date} and {end_date}")
    return orders