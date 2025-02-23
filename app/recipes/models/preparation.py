from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class Preparation(Base):
    __tablename__ = "preparation"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)

    # Chave estrangeira para a receita
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    # Relacionamento inverso
    recipe = relationship("Recipe", back_populates="preparations",lazy="joined")
