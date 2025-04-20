from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.config import Base

class Comment(Base):
    __tablename__ = "comment"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # 'index=True' melhora a performance de busca
    text = Column(String, nullable=False)  # Torne 'text' obrigatório, para garantir que o comentário tenha conteúdo
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="comments", lazy="joined")
    post_id = Column(Integer, ForeignKey("post.id"),index=True)
    post = relationship("Post", back_populates="comments")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
