from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.controllers.order_details import get_all_order_details, get_order_detail_by_id, update_order_detail
from api.schemas.order_details import OrderDetail


from ..schemas.order_details import OrderDetail
from api.dependencies.database import get_db


router = APIRouter(
    prefix="/orders/{order_id}/details",
    tags=["order_details"]
)

@router.get("/", response_model=list[OrderDetail])
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order_details = get_all_order_details(db, order_id)
    if not order_details:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    return order_details

@router.get("/{detail_id}", response_model=OrderDetail)
def get_order_detail(order_id: int, detail_id: int, db: Session = Depends(get_db)):
    order_detail = get_order_detail_by_id(db, order_id, detail_id)
    if not order_detail:
        raise HTTPException(status_code=404, detail=f"Order detail with ID {detail_id} not found for order {order_id}")
    return order_detail


@router.post("/", response_model=OrderDetail)
def create_order_detail(request: OrderDetail, order_id: int, db: Session = Depends(get_db)):
    return create_order_detail(request, order_id, db)


@router.put("/{detail_id}", response_model=OrderDetail)
def update_order_detail_route(
        order_id: int,
        detail_id: int,
        request: OrderDetail,
        db: Session = Depends(get_db)
):
    order_detail = update_order_detail(db, order_id, detail_id, request)

    if not order_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Order detail with ID {detail_id} not found for order {order_id}"
        )

    return order_detail


