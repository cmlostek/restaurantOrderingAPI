from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class OrderDetails(Base):
    __tablename__ = "order_details"
    detail_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    dish_id = Column(Integer, ForeignKey("menu.dish_id"))
    payment_id = Column(Integer, ForeignKey("payments.payment_id"))
    order_details = Column(String(300), nullable=False)
    order_status = Column(String(50), nullable=False)  # Pending, Completed, Canceled
    quantity = Column(Integer, nullable=False)
    ingredients = Column(String(300), nullable=False)  # Comma-separated list of ingredient IDs
