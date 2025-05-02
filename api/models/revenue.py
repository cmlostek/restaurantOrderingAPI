from datetime import date

from pydantic import BaseModel


class RevenueReport(BaseModel):
    sales_date: date
    total_revenue: float

    class Config:
        orm_mode = True