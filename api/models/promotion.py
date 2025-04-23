from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    promotion_id       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code               = Column(String(100), unique=True, nullable=False)
    description        = Column(String(200), nullable=True)
    discount_percentage= Column(Integer, nullable=False)
    valid_until        = Column(DateTime(timezone=True), nullable=False)
    payment_id         = Column(Integer, ForeignKey("payments.payment_id"), nullable=False)

    # relationships
    payment = relationship("Payment", back_populates="promotion", uselist=False)
