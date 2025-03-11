from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

from app.recipes.dtos.category_dto import CategoryDTO
from app.recipes.dtos.collection_dto import CollectionDTO
from app.recipes.dtos.image_dto import ImageDTO
from app.recipes.dtos.ingredient_dto import IngredientDTO
from app.recipes.dtos.preparation_dto import PreparationDTO

class DificultyEnum(str,Enum):
    facil = 'Fácil'
    medio = 'Médio'
    dificil = 'Difícil'
class RecipeCreateDTO(BaseModel):
    title: str
    images: List[ImageDTO]
    ingredients: List[IngredientDTO]
    preparations: List[PreparationDTO]
    description: str 
    session_id: Optional[int]
    categories:List[str]
    preparation_time: int
    #enum facil, medio, dificil
    dificulty: DificultyEnum
    portions : int
    class Config:
        orm_mode = True
        from_attributes = True
        

class RecipeRequestFilterDTO(BaseModel):
    query: Optional[str]
    categories: Optional[List[str]]
    size: int | None = 10
    page: int | None = 1
    
    class Config:
        orm_mode = True
        from_attributes = True

class IARecipeCreateDTO(BaseModel):
    title: str
    session_id: int
    
    
    class Config:
        orm_mode = True
        from_attributes = True

class RecipeResponseDTO(BaseModel):
    title: str
    images: List[ImageDTO]
    ingredients: List[IngredientDTO]
    preparations: List[PreparationDTO]
    description: str 
    session_id: Optional[int] | None 
    categories:List[str] | None = []
    preparation_time: int | None = 20
    #enum facil, medio, dificil
    dificulty: str | None = 'Fácil'
    portions : int | None = 1

    class Config:
        orm_mode = True

class RecipeListResponseDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]
    tumbnail: Optional[str]

    class Config:
        orm_mode = True