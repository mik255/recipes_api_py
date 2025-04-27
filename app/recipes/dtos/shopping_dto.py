

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class IngredientsAttDto(BaseModel):
    query: str
    id: Optional[int] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
        
class searchShoppingListDTO(BaseModel):
    query: str
    
    class Config:
        orm_mode = True
        from_attributes = True

class ShoppingItemsDTO(BaseModel):
    id: Optional[int] = None
    name: str
    quantity: Optional[float] = None
    unity: Optional[str] = None
    price: Optional[float] = None
    img: Optional[str] = None
    category: Optional[str] = None
    count: Optional[int] = None
    selected: Optional[bool] = None

    class Config:
        orm_mode = True

class PostShoppingListRequestDTO(BaseModel):
    name: str
    recipe_id: Optional[int] = None
    shopping_items: List[ShoppingItemsDTO] = []
    
    class Config:
        orm_mode = True
        
class ShoppingListResponseDTO(BaseModel):
    id: int
    name: str
    recipe_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    shopping_items: List[ShoppingItemsDTO] = []

    class Config:
        orm_mode = True
        from_attributes = True

