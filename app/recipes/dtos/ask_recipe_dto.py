
from pydantic import BaseModel


class AskRecipeDTO(BaseModel):
    description: str

    class Config:
        orm_mode = True