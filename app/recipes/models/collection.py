from sqlalchemy import Column, Float, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base

class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon_name = Column(String, nullable=False)

    # ForeignKey para indicar que cada coleção pertence a um único usuário
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relacionamento One-to-Many com User
    user = relationship("User", back_populates="collections")

    # Relacionamento Many-to-Many com Recipe
    recipes = relationship("Recipe", secondary="recipe_collection", back_populates="collections")




