from fastapi import APIRouter, Header,HTTPException, Depends, Query
from typing import List
from app.recipes.dtos.collection_dto import CollectionDTO, CollectionResponseDTO
from app.recipes.dtos.recipe_dto import RecipeListResponseDTO, RecipeResponseDTO
from app.recipes.services.collection_service import create, get_all_by_user_id, get_recipes, delete, update,remove_recipe_to_collection_service
from app.recipes.services.recipe_service import add_recipe_to_collection_service

router = APIRouter()

@router.post("/", response_model=CollectionResponseDTO, status_code=201)
def create_recipe_route(dto: CollectionDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:
        return create(dto, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    
@router.get("/", response_model=List[CollectionResponseDTO], status_code=200)
def get_recipe_by_id_route(
    user_id: int = Header(..., alias="X-User-Id")
):
    """
    Recupera o user_id do header 'X-User-Id' e retorna as receitas
    relacionadas a esse usuário.
    """
    try:
        return get_all_by_user_id(user_id=user_id)
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

#delete
@router.delete("/{collection_id}", status_code=204)
def delete_collection(collection_id: int):
    try:
        return delete(collection_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#update

@router.put("/{collection_id}", response_model=CollectionResponseDTO, status_code=200)
def update_collection(collection_id: int, dto: CollectionDTO):
    try:
        return update(collection_id, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.put("/{collection_id}/add_recipe/{recipe_id}", status_code=200)
def add_recipe_to_collection(collection_id: int, recipe_id: int):
    try:
        
        return add_recipe_to_collection_service(collection_id, recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
#remove recipe to colection
@router.delete("/{collection_id}/remove_recipe/{recipe_id}", status_code=200)
def remove_recipe_to_collection(collection_id: int, recipe_id: int):
    try:
        
        return remove_recipe_to_collection_service(collection_id =collection_id, recipe_id = recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")