from pydantic import BaseModel

class ImageDTO(BaseModel):
    url: str
    name: str | None = ''

    class Config:
        orm_mode = True
