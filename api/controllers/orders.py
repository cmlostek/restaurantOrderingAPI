from datetime import datetime

from sqlalchemy.orm import Session

from .users import OrderItem
from ..models.orders import Order
from ..schemas.orders import OrderSchema, GuestOrderCreate


def create_order(db: Session, request: OrderSchema):
    new_order = Order(**request.dict())
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


def create_guest_order(db: Session, request: GuestOrderCreate):
    new_order = Order(
        total_price=request.total_price,
        user_name="guest",  # Assuming guest orders don't have a user name
        user_id=None,  # Assuming guest orders don't have a user ID
        order_date=datetime.utcnow(),
        order_status="Pending",
        order_details="This is a guest order",
        dish_id=request.dish_id,
        order_id=None
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


    for item in request.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()

    return new_order