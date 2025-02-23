from sqlalchemy import Table, Column, Integer, ForeignKey, String
from app.database.config import Base

user_collection = Table(
    'user_collection',
    Base.metadata,
    Column('user_google_id', String, ForeignKey('user.google_id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collection.id'), primary_key=True)
)
