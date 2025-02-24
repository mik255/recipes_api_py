from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.recipes.dtos.recipe_dto import RecipeCreateDTO, RecipeListResponseDTO, RecipeResponseDTO
from app.recipes.dtos.session_dto import SessionResponseDTO 
from app.recipes.services.recipe_service import create_recipe_service, get_all_recipe_service, get_recipe_by_id_service,get_sessions


# Inicializa o roteador para o módulo Recipe
router = APIRouter()

# Rota para criar um novo REcipe
@router.post("/", response_model=RecipeResponseDTO, status_code=201)
def create_recipe_route(recipe: RecipeCreateDTO):

    try:
        return create_recipe_service(recipe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", response_model=List[RecipeListResponseDTO], status_code=200)
def list_recipe_route():
    try:
        return get_all_recipe_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    
@router.get("/{recipe_id}", response_model=RecipeResponseDTO, status_code=200)
def get_recipe_by_id_route(recipe_id: int):
    try:
        data = get_recipe_by_id_service(recipe_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")