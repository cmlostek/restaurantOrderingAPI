from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class OrderDetailCreate(BaseModel):
    order_id: int
    dish_id: int
    payment_id: int
    order_details: str
    order_status: str
    



class OrderDetailResponse(BaseModel):
    detail_id: int
    order_id: int
    dish_id: int
    payment_id: int
    order_details: str
    order_status: str

    class Config:
        orm_mode = True