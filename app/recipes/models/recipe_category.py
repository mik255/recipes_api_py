# models.py

from sqlalchemy import Table, Column, ForeignKey
from app.database.config import Base
recipe_categories = Table(
    'recipe_categories',
    Base.metadata,
    Column('recipe_id', ForeignKey('recipe.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)
)
