from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

menu_resources = Table(
    "menu_resources",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menu.dish_id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.resource_id"), primary_key=True),
)

class menu(Base):
    __tablename__ = "menu"

    dish_id = Column(Integer, primary_key=True)
    dish = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    ingredients = relationship("resources", secondary=menu_resources, backref="menus")
    calories = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)

