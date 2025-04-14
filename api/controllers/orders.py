from sqlalchemy.orm import Session
from ..models.orders import Order
from ..schemas.orders import OrderSchema

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