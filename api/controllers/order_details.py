from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas.order_details import  OrderDetail


def create_order_detail(db: Session, order_id: int, request: OrderDetail):
    new_order_detail = OrderDetail(**request.dict(), order_id=order_id)
    db.add(new_order_detail)
    db.commit()
    db.refresh(new_order_detail)
    return new_order_detail

def get_all_order_details(db: Session, order_id: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()

def get_order_detail_by_id(db: Session, order_id: int, detail_id: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.detail_id == detail_id).first()

def update_order_detail(db: Session, order_id: int, detail_id: int, request: OrderDetail):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.detail_id == detail_id).first()
    if order_detail:
        for key, value in request.dict().items():
            setattr(order_detail, key, value)
        db.commit()
        db.refresh(order_detail)
    return order_detail

def delete_order_detail(db: Session, order_id: int, detail_id: int):
    order_detail = db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.detail_id == detail_id).first()
    if order_detail:
        db.delete(order_detail)
        db.commit()
    return order_detail

def get_order_details_by_date(db: Session, order_id: int, date: datetime):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.date == date).all()

def get_order_details_by_status(db: Session, order_id: int, status: str):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.status == status).all()

def get_order_details_by_user(db: Session, order_id: int, user_id: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.user_id == user_id).all()

def get_order_details_by_item(db: Session, order_id: int, item_id: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.item_id == item_id).all()

def get_order_details_by_quantity(db: Session, order_id: int, quantity: int):
    return db.query(OrderDetail).filter(OrderDetail.order_id == order_id, OrderDetail.quantity == quantity).all()



