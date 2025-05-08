from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

user_review = Table(
    "user_review",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), unique = True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    user_role = Column(String(100), nullable=False)
    payment_info = Column(String(200), nullable=False)
    review = Column(String(200), nullable=True)
    rating = Column(String(10), nullable=True)

