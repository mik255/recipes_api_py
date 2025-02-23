from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    quantity = Column(String, nullable=False)  # Exemplo: "2 xícaras"

    # Chave estrangeira para a receita
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    # Relacionamento inverso
    recipe = relationship("Recipe", back_populates="ingredients",lazy="joined")
