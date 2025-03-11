from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.recipe_category import recipe_categories

class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, server_default="Sem descrição")
    preparation_time = Column(Float, nullable=False,server_default="0.0")
    serving_size = Column(Integer, nullable=False,server_default="0")
    dificulty = Column(String, nullable=False,server_default="Fácil")
    portions = Column(Integer, nullable=False,server_default="1")
    images = relationship("Image", back_populates="recipe", lazy="joined")
    ingredients = relationship("Ingredient", back_populates="recipe", lazy="joined")
    preparations = relationship("Preparation", back_populates="recipe", lazy="joined")
    session_id = Column(Integer, ForeignKey("session.id"))
    sessions = relationship("Session", secondary="session_recipe", back_populates="recipes")
    collections = relationship("Collection", secondary="recipe_collection", back_populates="recipes")
    # Relacionamento com Category via a tabela intermediária
    categories = relationship(
        "Category",
        secondary=recipe_categories,
        back_populates="recipes",
        lazy="joined"
    )