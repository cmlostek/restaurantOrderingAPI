from pydantic import BaseModel
from datetime import datetime

class PromotionBase(BaseModel):
    code:                str
    description:         str
    discount_percentage: int
    valid_until:         datetime

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(PromotionBase):
    pass

class PromotionSchema(PromotionBase):
    promotion_id: int

    class Config:
        orm_mode = True
