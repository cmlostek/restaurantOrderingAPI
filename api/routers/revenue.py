from datetime import datetime, date, time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.controllers.revenue import get_revenue_by_day
from api.dependencies.database import get_db
from api.models.orders import Order
from api.models.revenue import RevenueReport

router = APIRouter(prefix="/reports", tags=["reports"])



@router.get("/revenue/{day}", response_model=RevenueReport)
def read_daily_revenue(day: date, db: Session = Depends(get_db)):
    return get_revenue_by_day(db, day)
