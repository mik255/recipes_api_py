from sqlalchemy import Column, Integer, String
from app.database.config import Base
from app.recipes.models.recipe_category import recipe_categories
class AskRecipe(Base):
    __tablename__ = 'ask_recipe'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, unique=True, index=True)
