from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.recipes.models.recipe_category import recipe_categories
from pgvector.sqlalchemy import Vector

class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=False)
    description = Column(String, nullable=False, server_default="Sem descrição")
    preparation_time = Column(Float, nullable=False, server_default="0.0")
    serving_size = Column(Integer, nullable=False, server_default="0")
    dificulty = Column(String, nullable=False, server_default="Fácil")
    portions = Column(Integer, nullable=False, server_default="1")
    is_premium = Column(Boolean, nullable=False, server_default="0")
    images = relationship(
        "Image",
        back_populates="recipe",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    ingredients = relationship("Ingredient", back_populates="recipe", lazy="selectin")
    preparations = relationship("Preparation", back_populates="recipe", lazy="selectin")

    session_id = Column(Integer, ForeignKey("session.id"), index=True)
    collection_id = Column(Integer, ForeignKey("collection.id"), index=True)

    youtube_url = Column(String, nullable=True)
    property = Column(String, nullable=True)

    sessions = relationship("Session", back_populates="recipes", lazy="selectin")
    collection = relationship("Collection", back_populates="recipes")
    macro = relationship("Macro", back_populates="recipe", uselist=False, lazy="selectin")
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=True)
    user = relationship("User", back_populates="recipes", lazy="selectin")
    embedding = Column(Vector(3072), nullable=True)

    categories = relationship(
        "Category",
        secondary=recipe_categories,
        back_populates="recipes",
        lazy="joined"
    )

    # ✅ relacionamento reverso com Post (1:1)
    post = relationship(
        "Post",
        back_populates="recipe",
        uselist=False,
        lazy="joined"
    )
    
    shopping_lists = relationship(
        "ShoppingList",
        back_populates="recipe",
        lazy="selectin"
    )
    product_id = Column(Integer, ForeignKey("product.id"), index=True, nullable=True)
    product = relationship("Product", back_populates="recipes", lazy="selectin")
    

