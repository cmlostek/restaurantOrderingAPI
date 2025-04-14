from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    user_role = Column(String(100), nullable=False)
    payment_info = Column(String(100), nullable=False)
    review = Column(String(100))
    rating = Column(String(100))
