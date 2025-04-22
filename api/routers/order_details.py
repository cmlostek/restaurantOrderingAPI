from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/orders/{order_id}/details",
    tags=["order_details"]
)


# get method to retreive an orders details

@router.get("/", response_model=OrderSchema)
def read_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# post method to create an order details
# @router.post("/", response_model=OrderSchema)
# def create_new_order(request: OrderSchema, db: Session = Depends(get_db)):
#     return create_order(db, request)

# put method to update an order details
@router.put("/", response_model=OrderSchema)
def update_existing_order(order_id: int, request: OrderSchema, db: Session = Depends(get_db)):
    order = update_order(db, order_id, request)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# delete method to delete an order details
@router.delete("/", response_model=OrderSchema)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    order = delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
