from sqlalchemy import Column, Float, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", secondary="user_collection", back_populates="collection")
    icon_name = Column(String, nullable=False)
    recipes = relationship("Recipe", secondary="recipe_collection", back_populates="collections")
    users = relationship("User", secondary="user_collection", back_populates="collections")


