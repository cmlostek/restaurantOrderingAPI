from pydantic import BaseModel
from typing import List, Optional


class OrderDetail(BaseModel):
    detail_id: int
    order_id: int
    dish_id: int
    payment_id: int
    order_details: Optional[str]
    order_status: str  # Pending, Completed, Canceled

    class Config:
        orm_mode = True