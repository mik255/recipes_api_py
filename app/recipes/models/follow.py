from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database.config import Base

class Follow(Base):
    __tablename__ = "follows"  # Nome pluralizado da tabela

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    followed_user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    # Relacionamento com o usuário que segue
    follower = relationship("User", foreign_keys=[user_id], back_populates="following")

    # Relacionamento com o usuário seguido
    followed = relationship("User", foreign_keys=[followed_user_id], back_populates="followers")
