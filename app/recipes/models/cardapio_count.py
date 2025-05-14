from sqlalchemy import Column, Integer
from app.database.config import Base  # Ajuste o caminho se necessário

class ClickCounter(Base):
    __tablename__ = "click_counter"

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)