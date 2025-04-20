from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    
class Midia(Base):
    __tablename__ = "midia"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    type = Column(String)

