from typing import Optional
from pydantic import BaseModel

class IngredientDTO(BaseModel):
    title: str
    description: str
    quantity: Optional[float] = None
    unity: Optional[str] = None
    price: Optional[float] = None
    name: Optional[str] = None
    img: Optional[str] = None
    category: Optional[str] = None
    count: Optional[int] = None
    selected: Optional[bool] = None

    class Config:
        orm_mode = True
