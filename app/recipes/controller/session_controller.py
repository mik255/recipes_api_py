

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.recipes.dtos.recipe_dto import RecipeCreateDTO, RecipeListResponseDTO, RecipeResponseDTO
from app.recipes.dtos.session_dto import SessionRequestDTO, SessionResponseDTO
from app.recipes.models.recipe import Recipe
from app.recipes.services.session_service import create_session_service, get_recipes_by_session, get_recipes_by_session_id, get_sessions, add_recipe_to_session_service



# Inicializa o roteador para o módulo Recipe
router = APIRouter()

# Rota para criar um novo REcipe
@router.post("/create", status_code=201)
def create_session_route(dto: SessionRequestDTO):
    try:
        return create_session_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    
@router.get("/", response_model=List[SessionResponseDTO], status_code=200)
def get_session():
    try:
        response  = get_sessions()
        return [
            SessionResponseDTO(
                id=model_session.id,
                title=model_session.title,
                description=model_session.description,
                type=model_session.type,
                recipetype=model_session.recipeType,
                recipes=[
                    RecipeListResponseDTO(
                        id=recipe.id,
                        title=recipe.title,
                        description=recipe.description,
                        tumbnail=recipe.images[0].url if recipe.images else None,
                    )
                    for recipe in model_session.recipes
                ]
            )
            for model_session in response
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/{session_id}/recipes")
def get_recipes(session_id: int, size: int = 0, limit: int = 5):
    return get_recipes_by_session(session_id, size, limit)

@router.get("/recipes/{session_id}")
def get_recipes(session_id: int):
    return get_recipes_by_session_id(session_id)
# add recipe to session
@router.put("/{session_id}/add_recipe/{recipe_id}", status_code=200)
def add_recipe_to_session(session_id: int, recipe_id: int):
    try:
        return add_recipe_to_session_service(session_id, recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")