from datetime import date, datetime, time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session
from ..controllers.orders import (
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order,
    delete_order, filter_order_dates,
)
from ..models.orders import Order
from ..schemas.orders import OrderSchema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post("/", response_model=OrderSchema)
def create_new_order(request: OrderSchema, db: Session = Depends(get_db)):
    return create_order(db, request)

@router.get("/", response_model=list[OrderSchema])
def read_all_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)


@router.put("/{order_id}", response_model=OrderSchema)
def update_existing_order(order_id: int, request: OrderSchema, db: Session = Depends(get_db)):
    order = update_order(db, order_id, request)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}", response_model=OrderSchema)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    order = delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/by-range", response_model=List[OrderSchema])
def read_orders_by_range(
    start_date: date = Query(..., description="YYYY-MM-DD"),
    end_date:   date = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    return filter_order_dates(db, start_date, end_date)
