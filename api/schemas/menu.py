from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class menuSchema(BaseModel):
    dish_id: int
    dish: str
    price: float
    ingredients: str
    calories: int
    category: str
    promotion_code: str
    promotion_expiry: datetime

    class Config:
        orm_mode = True