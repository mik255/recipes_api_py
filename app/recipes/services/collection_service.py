from typing import List
from app.database.dependences import get_db
from app.recipes.dtos.collection_dto import CollectionDTO, CollectionResponseDTO
from app.recipes.dtos.recipe_dto import RecipeResponseDTO
from app.recipes.models.collection import Collection
from app.recipes.models.recipe import Recipe
from app.recipes.repository.collection_repository import create_collection, get_collections_by_user_id,get_recipes_collection


def create(dto: CollectionDTO,user_id:int) -> CollectionResponseDTO:

    with next(get_db()) as db:
        new_collection = Collection(
            name=dto.name,
            description=dto.description,
            icon_name=dto.icon_name,
            user_id=user_id)
    
        response = create_collection(db=db, collection=new_collection)
        return CollectionResponseDTO(
            id=response.id,
            name=response.name,
            description=response.description,
            icon_name=response.icon_name)


def get_all_by_user_id(user_id:int) -> list[CollectionDTO]:

    with next(get_db()) as db:
        colections = get_collections_by_user_id(db, user_id)
        return colections

def get_recipes(collection_id:int) -> List[RecipeResponseDTO]:
    with next(get_db()) as db:
        return get_recipes_collection(db, collection_id)
    
def delete(collection_id:int):
    with next(get_db()) as db:
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        return db.delete(collection)
    
def update(collection_id: int, dto: CollectionDTO):
    with next(get_db()) as db:
        collection = db.query(Collection).filter(Collection.id == collection_id).first()

        if not collection:
            raise ValueError(f"Collection with id {collection_id} not found.")

        collection.name = dto.name
        collection.description = dto.description
        collection.icon_name = dto.icon_name

        db.commit()
        db.refresh(collection)  # Atualiza a instância com os dados do banco

        return collection
