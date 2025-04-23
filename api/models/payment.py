from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    promotion_id  = Column(Integer, ForeignKey("promotions.promotion_id"), nullable=True)
    amount        = Column(DECIMAL(10, 2), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user       = relationship("User",       back_populates="payments")
    promotion  = relationship("Promotion",  back_populates="payment", uselist=False)
