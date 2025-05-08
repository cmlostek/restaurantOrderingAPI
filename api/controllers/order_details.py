from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..schemas.order_details import  OrderDetailCreate
from api.models.order_details import OrderDetails
from ..schemas.order_details import OrderDetailResponse



def create_new_order_detail(db: Session, order_id: int, request: OrderDetailCreate):
    order_detail = OrderDetails(
        order_id=order_id,
        dish_id=request.dish_id,
        payment_id=request.payment_id,
        order_details=request.order_details,
        order_status=request.order_status
    )
    db.add(order_detail)
    db.commit()
    db.refresh(order_detail)
    return order_detail


def get_all_order_details(db: Session, order_id: int):
    order_details = db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
    if not order_details:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order_details
 

def get_order_detail_by_id(db: Session, order_id: int, detail_id: int, response_model=OrderDetailResponse):
    order_detail = db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail=f"Order detail with ID {detail_id} not found for order {order_id}")
    return order_detail

def update_order_detail(db: Session, order_id: int, detail_id: int, request: OrderDetailCreate, response_model=OrderDetailResponse):
    order_detail = db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail=f"Order detail with ID {detail_id} not found for order {order_id}")

    order_detail.dish_id = request.dish_id
    order_detail.payment_id = request.payment_id
    order_detail.order_details = request.order_details
    order_detail.order_status = request.order_status

    db.commit()
    db.refresh(order_detail)
    return order_detail
 

def delete_order_detail(db: Session, order_id: int, detail_id: int, response_model=OrderDetailResponse):
    order_detail = db.query(OrderDetails).filter(OrderDetails.order_id == order_id, OrderDetails.detail_id == detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail=f"Order detail with ID {detail_id} not found for order {order_id}")

    db.delete(order_detail)
    db.commit()
    return order_detail


def delete_all_order_details(db: Session, order_id: int, response_model=List[OrderDetailResponse]):
    order_details = db.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
    if not order_details:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    for order_detail in order_details:
        db.delete(order_detail)
    db.commit()
    return order_details







