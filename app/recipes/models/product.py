
from typing import List
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.config import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "product"  # Nome correto da tabela

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(String, unique=True, index=False) #offer do google play
    title = Column(String, index=True)
    subtitle = Column(String, index=True)
    description = Column(String, index=True)
    bedge = Column(String, index=True)
    price = Column(Float, index=True)
    type = Column(String, index=True)
    benefts = Column(ARRAY(String))
    delta_expiration_in_days = Column(Integer, default=0)  # Delta de expiração em dias
    purchase_orders = relationship("PurchaseOrder", back_populates="product")
    recipes = relationship(
        "Recipe",
        back_populates="product",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
