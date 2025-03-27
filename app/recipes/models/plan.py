from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.config import Base

class Plan(Base):
    __tablename__ = "plan"  # Nome correto da tabela

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(String, unique=True, index=False)
    name = Column(String, index=True)
    description = Column(String, index=True)
    amount = Column(Float, index=True)
    
    # Relacionamento com Order (One-to-Many)
    orders = relationship("Order", back_populates="plan")
