from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.recipes.dtos.user_dto import UserResponseDTO, UserSaveRequestDTO
from app.recipes.services.users_service import create_user_service,verify_user_exists

# Inicializa o roteador para o módulo Recipe
router = APIRouter()

# Rota para criar um novo REcipe
@router.post("/login", response_model=UserResponseDTO, status_code=201)
def create_recipe_route(dto: UserSaveRequestDTO):
    try:
        is_exists = verify_user_exists(dto.google_id)
        if is_exists:
            return is_exists
        return create_user_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

