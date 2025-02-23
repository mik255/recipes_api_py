from typing import List, Optional
from pydantic import BaseModel

from app.recipes.dtos.recipe_dto import RecipeListResponseDTO

class SessionRequestDTO(BaseModel):
    title: str
    description: str
    recipes: List[str]
    type: str
    recipe_type: str

    class Config:
        orm_mode = True
        from_attributes = True
        
        
class SessionCreateDTO(BaseModel):
    title: str
    description: str
    type: str
    recipe_type: str

    class Config:
        orm_mode = True
        from_attributes = True
        
class SessionResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    type: str
    recipetype: str
    recipes: List[RecipeListResponseDTO]

    class Config:
        orm_mode = True
        from_attributes = True