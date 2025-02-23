from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.session_recipe import session_recipe

class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    recipeType = Column(String, nullable=False)
    recipes = relationship("Recipe", secondary=session_recipe, back_populates="sessions", lazy="joined")
    
    
