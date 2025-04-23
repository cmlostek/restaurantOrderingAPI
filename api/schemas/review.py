from pydantic import BaseModel
from typing import List, Optional

class Review(BaseModel):
    review_id: int
    user_id: int
    order_id: int
    rating: int
    comment: str

    class Config:
        orm_mode = True