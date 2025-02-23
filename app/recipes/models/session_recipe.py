from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.config import Base

session_recipe = Table(
    'session_recipe',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('session.id'), primary_key=True)
)

