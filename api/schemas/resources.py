from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class resourcesSchema(BaseModel):
    resource_id: int
    resource_name: str
    resource_type: str
    quantity_available: int

    class Config:
        orm_mode = True