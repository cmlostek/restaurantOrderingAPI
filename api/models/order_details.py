from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class OrderDetails(Base):
    __tablename__ = "order_details"

    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    dish_id = Column(Integer, ForeignKey("menu.dish_id"), primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.payment_id"), primary_key=True)
    order_details = Column(String(300), nullable=False)
    order_status = Column(String(50), nullable=False)  # Pending, Completed, Canceled
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    ingredients = Column(String(300), nullable=False)  # Comma-separated list of ingredient IDs