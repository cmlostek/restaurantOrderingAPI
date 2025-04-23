from pydantic import BaseModel
from typing import List, Optional

class usersSchema(BaseModel):
    user_id: int
    user_name: str
    email: str
    phone_number: int
    address: str
    user_role: str
    payment_info: str
    review: Optional[str]
    rating: Optional[str]
    payment_id: int


    class Config:
        orm_mode = True
