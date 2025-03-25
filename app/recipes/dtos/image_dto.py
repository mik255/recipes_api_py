from typing import Optional
from pydantic import BaseModel

class ImageDTO(BaseModel):
    url: str
    name: Optional[str] = None  # Corrigido para usar Optional[str] e valor padrão None

    class Config:
        from_attributes = True
