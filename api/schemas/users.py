from pydantic import BaseModel
from typing import Optional

class usersSchema(BaseModel):
    user_id: int
    user_name: str
    email: str
    phone: str
    address: str
    user_role: str
    payment_info: str
    review: Optional[str]
    rating: Optional[str]

    class Config:
        orm_mode = True