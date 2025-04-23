from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey("payment.payment_id"), nullable=False)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), unique = True, nullable=False)
    phone_number = Column(String(100), unique = True, nullable=False)
    address = Column(String(200), nullable=False)
    user_role = Column(String(100), nullable=False)

    payments = relationship("Payment", backref="user")