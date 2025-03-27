from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class Preparation(Base):
    __tablename__ = "preparation"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False)
    description = Column(String, nullable=True)
    step = Column(Integer, nullable=False, server_default="0")
    # Chave estrangeira para a receita
    recipe_id = Column(Integer, ForeignKey("recipe.id"),index=True)

    # Relacionamento inverso
    recipe = relationship("Recipe", back_populates="preparations",lazy="selectin")
