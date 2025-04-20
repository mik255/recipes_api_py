from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.recipes.dtos.user_dto import CreateCreatorRequestDTO, UserResponseDTO, UserSaveRequestDTO
from app.recipes.services.users_service import create_user_service, get_user_by_id_service, post_creators_service,verify_user_exists,get_creators_service

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


@router.get("/creators", response_model=List[UserResponseDTO])
def get_creators():
    try:
        return get_creators_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/creators", response_model=UserResponseDTO)
def post_creators(dto:CreateCreatorRequestDTO):
    try:
        return post_creators_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int):
    try:
        user = get_user_by_id_service(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")