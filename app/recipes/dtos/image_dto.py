from pydantic import BaseModel

class ImageDTO(BaseModel):
    url: str

    class Config:
        orm_mode = True
