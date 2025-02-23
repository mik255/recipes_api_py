from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.session_recipe import session_recipe

class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, server_default="Sem descrição")
    preparation_time = Column(Float, nullable=False,server_default="0.0")
    serving_size = Column(Integer, nullable=False,server_default="0")
    images = relationship("Image", back_populates="recipe", lazy="joined")
    ingredients = relationship("Ingredient", back_populates="recipe", lazy="joined")
    preparations = relationship("Preparation", back_populates="recipe", lazy="joined")
    sessions = relationship("Session", secondary="session_recipe", back_populates="recipes")
    collections = relationship("Collection", secondary="recipe_collection", back_populates="recipes")
