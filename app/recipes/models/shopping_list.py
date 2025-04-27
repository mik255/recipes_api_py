from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, func
from sqlalchemy.orm import relationship
from app.database.config import Base

class ShoppingList(Base):
    __tablename__ = "shopping_list"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    user = relationship(
        "User",
        back_populates="shopping_lists",
        lazy="selectin"
    )
    
    shopping_items = relationship(
        "Ingredient",
        back_populates="shopping_list",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    
    recipe_id = Column(Integer, ForeignKey("recipe.id"), index=True)
    recipe = relationship(
        "Recipe",
        back_populates="shopping_lists",
        lazy="selectin"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
