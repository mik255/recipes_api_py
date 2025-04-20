from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.recipes.dtos.comment_dto import CommentResponseDTO
from app.recipes.dtos.image_dto import ImageDTO


class PostCreateDTO(BaseModel):
    description: Optional[str] = None
    recipe_id: Optional[int] = None


class UserPostDTO(BaseModel):
    id: int
    name: str
    photo_url: Optional[str] = None
    creator_nick_name: Optional[str] = None

    class Config:
        orm_mode = True
        
class RecipePostDTO(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    preparation_time: Optional[int] = None
    images: List[ImageDTO]

    class Config:
        orm_mode = True
        
class LikePostDTO(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class PostResponseDTO(BaseModel):
    id: int
    user: UserPostDTO
    recipe: RecipePostDTO
    description: Optional[str] = None
    media_id: Optional[int] = None
    created_at: datetime
    likes: List[LikePostDTO]
    comments: List[CommentResponseDTO]

    model_config = {
        "from_attributes": True  # substitui orm_mode = True
    }
    
class PaginedPostResponseDTO(BaseModel):
    posts: List[PostResponseDTO]
    total: int
    page: int
    size: int

    class Config:
        orm_mode = True