from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.recipe_category import recipe_categories
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=False)
    
    recipes = relationship(
        "Recipe",
        secondary=recipe_categories,
        back_populates="categories",
        lazy="joined"
    )