

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List

from app.recipes.dtos.shopping_dto import PostShoppingListRequestDTO, ShoppingListResponseDTO
from app.recipes.services.shopping_service import create_shopping_list_service, delete_shopping_list_service, get_shopping_list_by_id_service, get_shopping_list_service, update_shopping_list_service

# Inicializa o roteador para o módulo Recipe
router = APIRouter()

# Rota para criar um novo REcipe
@router.post("/", response_model=ShoppingListResponseDTO, status_code=201)
def create_recipe_route(dto: PostShoppingListRequestDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:
     return create_shopping_list_service(dto,user_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/list", response_model=List[ShoppingListResponseDTO], status_code=200)
def get_shopping_list_route(user_id: int = Header(..., alias="X-User-Id")):
    try:
        return get_shopping_list_service(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.delete("/item/{id}", response_model=ShoppingListResponseDTO, status_code=200)
def delete_shopping_list_route(id: int):
    try:
        return delete_shopping_list_service(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/item/{id}", response_model=ShoppingListResponseDTO, status_code=200)
def get_shopping_list_by_id_route(id: int):
    try:
        return get_shopping_list_by_id_service(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/item/{id}", response_model=ShoppingListResponseDTO, status_code=200)
def update_shopping_list_route(id: int, dto: PostShoppingListRequestDTO):
    try:
        return update_shopping_list_service(id, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    

