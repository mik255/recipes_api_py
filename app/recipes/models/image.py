from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base  # Ajuste o caminho conforme sua estrutura

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id", ondelete="CASCADE"), index=True)
    name = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="images", lazy="selectin")
