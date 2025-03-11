from pydantic import BaseModel

class IngredientDTO(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
