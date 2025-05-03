from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderCreate(BaseModel):
    user_id: Optional[int]
    dish_id: int
    order_date: datetime
    total_price: float
    is_guest: int


class OrderResponse(BaseModel):
    order_id: int
    user_id: Optional[int]
    dish_id: int
    order_date: datetime
    total_price: float
    is_guest: int

    class Config:
        orm_mode = True
