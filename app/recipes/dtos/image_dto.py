from typing import Optional
from pydantic import BaseModel

class ImageDTO(BaseModel):
    url: str
    name: Optional[str] | None

    class Config:
        orm_mode = True
