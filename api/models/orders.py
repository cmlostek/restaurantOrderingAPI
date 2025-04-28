from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("menu.dish_id"))
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    total_price = Column(DECIMAL(10, 2))
    is_guest = Column(Integer, default=False)
