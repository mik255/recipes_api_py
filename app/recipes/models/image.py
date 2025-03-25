from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    name = Column(String, nullable=True)  # Certifique-se de que o campo existe

    recipe = relationship("Recipe", back_populates="images",lazy="joined")
