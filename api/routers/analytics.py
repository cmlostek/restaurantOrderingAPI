from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.controllers.analytics import (
    get_revenue_by_period,
    get_top_dishes,
    get_top_customers,
    get_sales_trends,
    get_category_performance,
    get_overview_stats
)
from api.dependencies.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """Get overall statistics for the admin dashboard"""
    return get_overview_stats(db)


@router.get("/revenue")
def get_revenue_analytics(start_date: date, end_date: date, db: Session = Depends(get_db)):
    """Get revenue statistics for a date range"""
    return get_revenue_by_period(db, start_date, end_date)


@router.get("/top-dishes")
def get_popular_dishes(limit: int = 10, db: Session = Depends(get_db)):
    """Get top selling dishes"""
    return get_top_dishes(db, limit)


@router.get("/top-customers")
def get_best_customers(limit: int = 10, db: Session = Depends(get_db)):
    """Get top spending customers"""
    return get_top_customers(db, limit)


@router.get("/sales-trends")
def get_trends(days: int = 7, db: Session = Depends(get_db)):
    """Get sales trends for the last N days"""
    return get_sales_trends(db, days)


@router.get("/category-performance")
def get_categories(db: Session = Depends(get_db)):
    """Get revenue performance by category"""
    return get_category_performance(db)
