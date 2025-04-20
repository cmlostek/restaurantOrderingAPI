from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    dish_id = Column(Integer, ForeignKey("menu.dish_id"))
    user_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    order_status = Column(String(50))
    total_price = Column(DECIMAL(10, 2))
    order_details = Column(String(300))

