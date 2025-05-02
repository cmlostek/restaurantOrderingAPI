from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    user_id:      int
    promotion_id: Optional[int]
    amount:       float

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class PaymentSchema(PaymentBase):
    payment_id:  int
    created_at:  datetime

    class Config:
        orm_mode = True
