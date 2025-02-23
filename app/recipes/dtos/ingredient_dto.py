from pydantic import BaseModel

class IngredientDTO(BaseModel):
    title: str
    quantity: str

    class Config:
        orm_mode = True
