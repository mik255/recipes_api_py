from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.config import Base

recipe_collection = Table(
    'recipe_collection',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collection.id'), primary_key=True)
)
