from pydantic import BaseModel
from typing import List, Optional

class usersCreate(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str
    address: str
    user_role: str
    payment_info: str
    review: Optional[str] = None
    rating: Optional[str] = None


class usersResponse(BaseModel):
    user_id: int
    username: str
    email: str
    phone_number: str
    address: str
    user_role: str
    payment_info: str
    review: Optional[str]
    rating: Optional[str]
    # Note: password is excluded from response for security
    

    class Config:
        orm_mode = True

class usersLogin(BaseModel):
    username: str
    password: str
