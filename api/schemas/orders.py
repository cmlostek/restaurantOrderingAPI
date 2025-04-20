from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderSchema(BaseModel):
    order_id: int
    user_id: int
    dish_id: int
    user_name: str
    order_date: datetime
    order_status: str
    total_price: float
    order_details: Optional[str]

    class Config:
        orm_mode = True

class GuestOrderItem(BaseModel):
    product_id: int
    quantity: int

class GuestOrderCreate(BaseModel):
    items: List[GuestOrderItem]
    dish_id: int
    total_price: float
    guest_email: str