from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False, nullable=True)
    description = Column(String, nullable=False, server_default="Sem descrição")
    # Chave estrangeira para a receita
    recipe_id = Column(Integer, ForeignKey("recipe.id"), index=True, nullable=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_list.id"), index=True, nullable=True)

    # Relacionamento inverso
    recipe = relationship("Recipe", back_populates="ingredients", lazy="selectin")
    shopping_list = relationship("ShoppingList", back_populates="shopping_items", lazy="selectin")
    
    quantity = Column(Integer, nullable=False, server_default="0")
    unity = Column(String, nullable=False, server_default="")
    price = Column(Float, nullable=False, server_default="0.0")
    name = Column(String, nullable=False, server_default="sem nome")
    img = Column(String, nullable=True)
    category = Column(String, nullable=True)
    count = Column(Integer, nullable=False, server_default="1")
    selected = Column(Boolean, nullable=False, server_default="0")


    