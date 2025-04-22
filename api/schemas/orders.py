from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderSchema(BaseModel):
    order_id: int
    user_id: int
    dish_id: int
    order_date: datetime
    order_status: str
    total_price: float
    order_details: Optional[str]
    is_guest: bool = False

    class Config:
        orm_mode = True
