from datetime import datetime, date, time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.orders import Order
from api.models.revenue import RevenueReport


def get_revenue_by_day(db: Session, day: date):
    start = datetime.combine(day, time.min)
    end   = datetime.combine(day, time.max)

    orders_q = (
        db.query(Order)
          .filter(Order.order_date >= start, Order.order_date <= end)
          .all()
    )

    total = round(sum(float(o.total_price) for o in orders_q), 2)

    return RevenueReport(sales_date=day, total_revenue=total)