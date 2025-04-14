from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class menu(Base):
    __tablename__ = "menu"

    dish_id = Column(Integer, primary_key=True)
    dish = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    ingredients = Column(String(300), nullable=False)
    calories = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
    promotion_code = Column(String(100), nullable=False)
    promotion_expiry = Column(DATETIME, nullable=False)

