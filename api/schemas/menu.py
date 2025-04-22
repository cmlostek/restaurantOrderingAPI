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

    class Config:
        orm_mode = True