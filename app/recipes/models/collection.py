from sqlalchemy import Column, Float, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base

class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)

    # ForeignKey para indicar que cada coleção pertence a um único usuário
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    recipes = relationship("Recipe", back_populates="collection", lazy="joined")
    user = relationship("User", back_populates="collections", lazy="joined")




