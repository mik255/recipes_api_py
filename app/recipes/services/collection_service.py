from typing import List
from app.database.dependences import get_db
from app.recipes.dtos.collection_dto import CollectionDTO, CollectionResponseDTO
from app.recipes.dtos.recipe_dto import RecipeResponseDTO
from app.recipes.models.collection import Collection
from app.recipes.models.recipe import Recipe
from app.recipes.repository.collection_repository import create_collection, get_collections_by_user_id,get_recipes_collection


def create(dto: CollectionDTO) -> CollectionResponseDTO:

    with next(get_db()) as db:
        new_collection = Collection(
            name=dto.name,
            description=dto.description,
            icon_name=dto.icon_name,
            user_id=dto.user_id)
    
        response = create_collection(db=db, collection=new_collection)
        return CollectionResponseDTO(
            id=response.id,
            name=response.name,
            description=response.description,
            icon_name=response.icon_name)


def get_all_by_user_id(google_id:str) -> list[CollectionDTO]:

    with next(get_db()) as db:
        colections = get_collections_by_user_id(db, google_id)
        return colections

def get_recipes(collection_id:int) -> List[RecipeResponseDTO]:
    with next(get_db()) as db:
        return get_recipes_collection(db, collection_id)