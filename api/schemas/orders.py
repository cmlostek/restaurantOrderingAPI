from pydantic import BaseModel
from typing import Optional
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