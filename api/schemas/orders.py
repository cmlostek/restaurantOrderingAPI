from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderSchema(BaseModel):
    order_id: int
    user_id: int
    dish_id: int
    order_date: datetime
    total_price: float
    is_guest: bool = False

    class Config:
        orm_mode = True
