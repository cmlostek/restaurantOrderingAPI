from datetime import datetime, date, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.orders import Order
from api.models.menu import menu
from api.models.users import User
from api.models.review import Review as ReviewModel


def get_revenue_by_period(db: Session, start_date: date, end_date: date) -> Dict:
    """Get revenue for a date range"""
    start = datetime.combine(start_date, datetime.min.time())
    end = datetime.combine(end_date, datetime.max.time())
    
    orders = db.query(Order).filter(
        Order.order_date >= start,
        Order.order_date <= end
    ).all()
    
    total_revenue = sum(float(o.total_price) for o in orders)
    order_count = len(orders)
    avg_order_value = total_revenue / order_count if order_count > 0 else 0
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": round(total_revenue, 2),
        "order_count": order_count,
        "average_order_value": round(avg_order_value, 2)
    }


def get_top_dishes(db: Session, limit: int = 10) -> List[Dict]:
    """Get most popular dishes by order count"""
    dish_orders = (
        db.query(
            Order.dish_id,
            func.count(Order.order_id).label('order_count'),
            func.sum(Order.total_price).label('total_revenue')
        )
        .group_by(Order.dish_id)
        .order_by(func.count(Order.order_id).desc())
        .limit(limit)
        .all()
    )
    
    # Get dish names
    dishes = db.query(menu).all()
    dish_dict = {d.dish_id: d.dish for d in dishes}
    
    result = []
    for dish_id, order_count, total_revenue in dish_orders:
        result.append({
            "dish_id": dish_id,
            "dish_name": dish_dict.get(dish_id, "Unknown"),
            "order_count": order_count,
            "total_revenue": round(float(total_revenue) if total_revenue else 0, 2)
        })
    
    return result


def get_top_customers(db: Session, limit: int = 10) -> List[Dict]:
    """Get top customers by total spending"""
    customer_orders = (
        db.query(
            Order.user_id,
            func.count(Order.order_id).label('order_count'),
            func.sum(Order.total_price).label('total_spent')
        )
        .filter(Order.user_id.isnot(None))
        .group_by(Order.user_id)
        .order_by(func.sum(Order.total_price).desc())
        .limit(limit)
        .all()
    )
    
    # Get user information
    users = db.query(User).all()
    user_dict = {u.user_id: u.username for u in users}
    
    result = []
    for user_id, order_count, total_spent in customer_orders:
        result.append({
            "user_id": user_id,
            "username": user_dict.get(user_id, "Unknown"),
            "order_count": order_count,
            "total_spent": round(float(total_spent) if total_spent else 0, 2)
        })
    
    return result


def get_sales_trends(db: Session, days: int = 7) -> List[Dict]:
    """Get daily sales trends for the last N days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    trends = []
    current_date = start_date
    
    while current_date <= end_date:
        start = datetime.combine(current_date, datetime.min.time())
        end = datetime.combine(current_date, datetime.max.time())
        
        orders = db.query(Order).filter(
            Order.order_date >= start,
            Order.order_date <= end
        ).all()
        
        revenue = sum(float(o.total_price) for o in orders)
        
        trends.append({
            "date": current_date,
            "revenue": round(revenue, 2),
            "order_count": len(orders)
        })
        
        current_date += timedelta(days=1)
    
    return trends


def get_category_performance(db: Session) -> List[Dict]:
    """Get revenue by menu category"""
    orders = db.query(Order).join(menu).all()
    
    category_stats = {}
    for order in orders:
        dish = db.query(menu).filter(menu.dish_id == order.dish_id).first()
        if dish:
            category = dish.category
            if category not in category_stats:
                category_stats[category] = {"revenue": 0, "order_count": 0}
            
            category_stats[category]["revenue"] += float(order.total_price)
            category_stats[category]["order_count"] += 1
    
    result = []
    for category, stats in category_stats.items():
        result.append({
            "category": category,
            "revenue": round(stats["revenue"], 2),
            "order_count": stats["order_count"]
        })
    
    # Sort by revenue descending
    result.sort(key=lambda x: x["revenue"], reverse=True)
    
    return result


def get_overview_stats(db: Session) -> Dict:
    """Get overall statistics"""
    total_users = db.query(User).count()
    total_orders = db.query(Order).count()
    total_revenue = db.query(func.sum(Order.total_price)).scalar() or 0
    avg_rating = db.query(func.avg(ReviewModel.rating)).scalar() or 0
    
    # Today's stats
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    
    today_orders = db.query(Order).filter(
        Order.order_date >= start,
        Order.order_date <= end
    ).count()
    
    today_revenue = db.query(func.sum(Order.total_price)).filter(
        Order.order_date >= start,
        Order.order_date <= end
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_orders": total_orders,
        "total_revenue": round(float(total_revenue), 2),
        "average_rating": round(float(avg_rating), 2),
        "today_orders": today_orders,
        "today_revenue": round(float(today_revenue), 2)
    }
