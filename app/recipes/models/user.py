from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    photo_url = Column(String, index=True)
    name = Column(String, index=True)
    
    # Relacionamento Many-to-Many com Collection
    collections = relationship("Collection", back_populates="user")
    orders = relationship("Order", back_populates="user")
        # Relacionamento Many-to-One com Plan (um usuário tem um plano)
    plan_id = Column(Integer, ForeignKey("plan.id"))  # Adicionando chave estrangeira para Plan
    plan = relationship("Plan", back_populates="users")

