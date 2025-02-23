from typing import List, Optional
from pydantic import BaseModel

from app.recipes.dtos.image_dto import ImageDTO
from app.recipes.dtos.ingredient_dto import IngredientDTO
from app.recipes.dtos.preparation_dto import PreparationDTO

class RecipeCreateDTO(BaseModel):
    title: str
    images: List[ImageDTO]
    ingredients: List[IngredientDTO]
    preparations: List[PreparationDTO]
    description: str 
    preparation_time: float
    serving_size: int
    
    
    class Config:
        orm_mode = True
        from_attributes = True

class RecipeResponseDTO(BaseModel):
    id: int
    title: str
    images: List[ImageDTO]
    ingredients: List[IngredientDTO]
    preparations: List[PreparationDTO]

    class Config:
        orm_mode = True

class RecipeListResponseDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]
    tumbnail: Optional[str]

    class Config:
        orm_mode = True