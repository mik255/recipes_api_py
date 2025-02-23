from pydantic import BaseModel

class PreparationDTO(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
