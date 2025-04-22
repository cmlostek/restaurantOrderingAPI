from pydantic import BaseModel
from typing import List, Optional


class OrderDetail(BaseModel):
    order_id: int
    dish_id: int
    payment_id: int
    order_details: Optional[str]
    order_status: str  # Pending, Completed, Cancelled

    class Config:
        orm_mode = True