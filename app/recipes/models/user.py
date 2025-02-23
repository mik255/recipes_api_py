from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base  # Certifique-se de que o caminho está correto

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String,unique=True, index=True)
    email = Column(String, index=True)
    photo_url = Column(String, index=True)
    name = Column(String, index=True)
    collections = relationship("Collection", secondary="user_collection", back_populates="users")
    