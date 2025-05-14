from sqlalchemy import Column, Integer, String
from app.database.config import Base  # Ajuste conforme a sua estrutura de projeto

class ContactMessage(Base):
    __tablename__ = "contact_message"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    restaurante = Column(String, nullable=False)
    mensagem = Column(String, nullable=False)
