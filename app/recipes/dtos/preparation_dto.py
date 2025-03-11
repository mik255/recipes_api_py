from pydantic import BaseModel

class PreparationDTO(BaseModel):
    title: str
    description: str
    step: int

    class Config:
        orm_mode = True
