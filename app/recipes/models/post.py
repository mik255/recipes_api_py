from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.config import Base

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all", lazy="selectin")
    likes = relationship("Like", back_populates="post", cascade="all", lazy="selectin")

    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipe = relationship(
        "Recipe",
        back_populates="post",
        foreign_keys=[recipe_id],
        lazy="selectin"
    )
