from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas.order_details import  OrderDetail
from api.models.order_details import OrderDetails


def create_new_order_detail(db: Session, order_id: int, request: OrderDetail):
    data = request.dict()
    data["order_id"] = order_id
    new_order_detail = OrderDetails(**data)
    db.add(new_order_detail)
    db.commit()
    db.refresh(new_order_detail)
    return new_order_detail

def get_all_order_details(db: Session, order_id: int):
    return db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()

def get_order_detail_by_id(db: Session, order_id: int, detail_id: int):
    return db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()

def update_order_detail(db: Session, order_id: int, detail_id: int, request: OrderDetail):
    order_detail = db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()
    if order_detail:
        for key, value in request.dict().items():
            setattr(order_detail, key, value)
        db.commit()
        db.refresh(order_detail)
    return order_detail


def delete_order_detail(db: Session, order_id: int, detail_id: int):
    order_detail = db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()
    if order_detail:
        db.delete(order_detail)
        db.commit()
    return order_detail

def delete_all_order_details(db: Session, order_id: int):
    order_details = db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
    if order_details:
        for detail in order_details:
            db.delete(detail)
        db.commit()
    return order_details






