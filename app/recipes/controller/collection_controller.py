from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.recipes.dtos.collection_dto import CollectionDTO, CollectionResponseDTO
from app.recipes.dtos.recipe_dto import RecipeListResponseDTO, RecipeResponseDTO
from app.recipes.services.collection_service import create, get_all_by_user_id, get_recipes

router = APIRouter()

@router.post("/", response_model=CollectionResponseDTO, status_code=201)
def create_recipe_route(dto: CollectionDTO):
    try:
        return create(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    
@router.get("/", response_model=List[CollectionResponseDTO], status_code=200)
def get_recipe_by_id_route(google_id: str = Query(...)):
    try:
        return get_all_by_user_id(google_id=google_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/recipes", response_model=List[RecipeListResponseDTO], status_code=200)
def get_recipe_by_id_route(collection_id: int = Query(...)):
    try:
        recipes: List[RecipeResponseDTO] = get_recipes(collection_id=collection_id)
        response = [
            RecipeListResponseDTO(
                id=item.id,
                title=item.title,
                description=item.description,
                tumbnail=item.images[0].url
            )
            for item in recipes
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
