from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

payment_promo = Table(
    "payment_promo",
    Base.metadata,
    Column("payment_id", Integer, ForeignKey("payments.payment_id"), primary_key=True),
    Column("promotion_id", Integer, ForeignKey("promotions.promotion_id"), primary_key=True),
)

class Payment(Base):
    __tablename__ = "payments"

    payment_id    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    promotion_id  = Column(Integer, ForeignKey("promotions.promotion_id"), nullable=True)
    amount        = Column(DECIMAL(10, 2), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
