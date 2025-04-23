from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = 'review'
    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=False)
