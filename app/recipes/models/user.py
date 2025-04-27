from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)  # Criei um índice aqui, caso você pesquise com frequência por email
    photo_url = Column(String, index=False)
    name = Column(String, index=True)  # Adicionei um índice aqui, caso você precise buscar usuários pelo nome

    collections = relationship("Collection", back_populates="user")
    orders = relationship("Order", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")

    # Relacionamentos de seguidores e seguindo
    followers = relationship("Follow", foreign_keys="[Follow.followed_user_id]", back_populates="followed")
    following = relationship("Follow", foreign_keys="[Follow.user_id]", back_populates="follower")
    creator_nick_name = Column(String, index=True,nullable=True)  # Adicionei um índice aqui, caso você precise buscar usuários pelo nome do criador
    creator_start_at = Column(DateTime(timezone=True), nullable=True)
    recipes = relationship("Recipe", back_populates="user")
    shopping_lists = relationship("ShoppingList", back_populates="user")