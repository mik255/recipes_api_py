from sqlalchemy import Column, ForeignKey, Integer, String,Float
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.recipe_category import recipe_categories

class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False)
    description = Column(String, nullable=False, server_default="Sem descrição")
    preparation_time = Column(Float, nullable=False,server_default="0.0")
    serving_size = Column(Integer, nullable=False,server_default="0")
    dificulty = Column(String, nullable=False,server_default="Fácil")
    portions = Column(Integer, nullable=False,server_default="1")
    images = relationship("Image", back_populates="recipe", lazy="selectin")
    ingredients = relationship("Ingredient", back_populates="recipe", lazy="selectin")
    preparations = relationship("Preparation", back_populates="recipe", lazy="selectin")
    session_id = Column(Integer, ForeignKey("session.id"),index=True)
    collection_id = Column(Integer, ForeignKey("collection.id"),index=True)
    youtube_url = Column(String, nullable=True)
    property = Column(String, nullable=True)
    sessions = relationship("Session", back_populates="recipes", lazy="selectin")
    collection = relationship("Collection", back_populates="recipes")
    macro = relationship(
        "Macro",
        back_populates="recipe",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    categories = relationship(
        "Category",
        secondary=recipe_categories,
        back_populates="recipes",
        lazy="joined"
    )