from pydantic import BaseModel
from typing import Optional


from enum import Enum

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
# DTO para a resposta da mídia
class MediaResponseDTO(BaseModel):
    id: int
    url: str
    type: str
    post_id: Optional[int] = None  # Se a mídia estiver associada a um post

    class Config:
        orm_mode = True

# DTO para salvar a mídia
class MediaSaveRequestDTO(BaseModel):
    url: str
    type: MediaType
    
    
