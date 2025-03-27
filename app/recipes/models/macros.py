from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from app.database.config import Base

class Macro(Base):
    __tablename__ = "macro"

    id = Column(Integer, primary_key=True, index=True)

    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False,index=True)

    total_kcal = Column(Float, nullable=False, server_default="0.0")
    percent_kcal = Column(Float, nullable=False, server_default="0.0")  # Ex: 80% do total diário

    carb_percent = Column(Float, nullable=False, server_default="0.0")     # Ex: 30%
    protein_percent = Column(Float, nullable=False, server_default="0.0")  # Ex: 60%
    fiber_percent = Column(Float, nullable=False, server_default="0.0")    # Ex: 20%
    fat_percent = Column(Float, nullable=False, server_default="0.0")      # Ex: 20%

    recipe = relationship("Recipe", back_populates="macro")
