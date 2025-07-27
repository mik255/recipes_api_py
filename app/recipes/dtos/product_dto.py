


from typing import Optional
from pydantic import BaseModel

from app.recipes.dtos.recipe_dto import RecipeListResponseDTO, RecipeResponseDTO

    

class ProductResponseDTO(BaseModel):
    id: int
    offer_id: str
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    bedge: Optional[str] = None
    price: float
    type: str
    benefts: Optional[list[str]] = None,
    recipes: Optional[list[RecipeListResponseDTO]] = None

    class Config:
        from_attributes=True

class AddRecipeToProductDTO(BaseModel):
    product_id: int
    recipe_id: int
    class Config:
        from_attributes=True