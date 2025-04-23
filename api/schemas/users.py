from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_id: int
    user_name: str
    email: str
    phone_number: int
    address: str
    user_role: str
    payment_id: int


    class Config:
        orm_mode = True
