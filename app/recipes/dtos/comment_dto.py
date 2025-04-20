from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.recipes.dtos.user_dto import UserResponseDTO

# DTO para a resposta do comentário, com informações do usuário e do post
class CommentResponseDTO(BaseModel):
    id: int
    text: str
    post_id: int
    user: Optional[UserResponseDTO] = None  # Informações do usuário que fez o comentário

    class Config:
        orm_mode = True  # Permite que o Pydantic use o modelo ORM diretamente


class CommentCreateDTO(BaseModel):
    text: str  # O texto do comentário, obrigatoriamente
    post_id: int  # ID do post ao qual o comentário se refere

    class Config:
        orm_mode = True  # Permite que o Pydantic use o modelo ORM diretamente