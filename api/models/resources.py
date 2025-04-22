from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class resources(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resource_name = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)