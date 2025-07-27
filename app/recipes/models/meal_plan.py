from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from app.database.config import Base

class MealPlan(Base):
    __tablename__ = "meal_plan"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id", ondelete="CASCADE"), nullable=False, index=True)
    
