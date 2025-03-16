import os
from typing import List
from app.database.dependences import get_db
from app.recipes.dtos.ask_recipe_dto import AskRecipeDTO
from app.recipes.dtos.recipe_dto import RecipeCreateDTO, RecipeListResponseDTO, RecipeRequestFilterDTO
from app.recipes.dtos.session_dto import SessionResponseDTO
from app.recipes.models.ask_recipe import AskRecipe
from app.recipes.models.category import Category
from app.recipes.models.recipe import Recipe
from app.recipes.models.ingredient import Ingredient
from app.recipes.models.preparation import Preparation
from app.recipes.models.image import Image
from app.recipes.models.session import Session
from app.recipes.repository.collection_repository import get_collection_by_id
from app.recipes.repository.recipe_repository import get_all_recipes, get_recipe_by_id, get_all_sessions
from meilisearch import Client

# 1) Conexão com Meilisearch
# Carregar variáveis de ambiente do SSM
MEILI_URL = os.getenv("MEILI_URL")  # Fallback padrão se não carregar
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")  # Fallback padrão

client = Client(MEILI_URL, MEILI_MASTER_KEY)

# 2) Criar (ou obter) o índice chamado "recipes"
index = client.index("recipes")

def configure_meilisearch():
    client.create_index("recipes", {"primaryKey": "id"})
    index.update_settings({
                "filterableAttributes": ["categories", "ingredients_keywords","property"],
        "searchableAttributes": ["title", "description", "ingredients_text"]
    })
   
    print("Filterable attributes configurados com sucesso!")

configure_meilisearch()

def create_recipe_service(recipe_dto: RecipeCreateDTO) -> Recipe:
    db = next(get_db())

    new_recipe = Recipe(
        title=recipe_dto.title,
        description=recipe_dto.description,
        session_id=recipe_dto.session_id,
        preparation_time=recipe_dto.preparation_time,
        dificulty=recipe_dto.dificulty,
        portions=recipe_dto.portions,
        youtube_url=recipe_dto.youtube_url,
        property=recipe_dto.property,
    )
    
    new_recipe.images = [Image(**image.model_dump()) for image in recipe_dto.images]
    new_recipe.ingredients = [Ingredient(**ingredient.model_dump()) for ingredient in recipe_dto.ingredients]
    new_recipe.preparations = [Preparation(**prep.model_dump()) for prep in recipe_dto.preparations]

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    ingredients_list = [ing.title for ing in new_recipe.ingredients]
    ingredients_text = ", ".join(ingredients_list)
    ingredients_keywords = [ing.lower().strip() for ing in ingredients_list]

    doc = {
        "id": new_recipe.id,
        "title": new_recipe.title,
        "description": new_recipe.description,
        "categories": [cat.name for cat in new_recipe.categories],
        "images": [img.url for img in new_recipe.images] if new_recipe.images else [],
        "preparation_time": new_recipe.preparation_time,
        "dificulty": new_recipe.dificulty,
        "portions": new_recipe.portions,
        "ingredients": ingredients_list,
        "ingredients_text": ingredients_text,
        "ingredients_keywords": ingredients_keywords,
        "preparations": [prep.title for prep in new_recipe.preparations],
        "session_id": new_recipe.session_id,
    }

    try:
        index.add_documents([doc])
    except Exception as e:
        print(f"Erro ao indexar receita {new_recipe.id} no Meilisearch: {e}")

    return new_recipe



def get_all_recipe_service() -> list[RecipeListResponseDTO]:
    """
    Serviço para listar todas as receitas.
    :return: Lista de objetos RecipeListResponseDTO representando as receitas.
    """
    with next(get_db()) as db:
        recipes = get_all_recipes(db)
        return [
            RecipeListResponseDTO(
                id=recipe.id,
                title=recipe.title,
                description=recipe.description,
                tumbnail=recipe.images[0].url if recipe.images else None,
                property=recipe.property
            )
            for recipe in recipes
        ]


def get_recipe_by_id_service(recipe_id: int) -> dict:

    with next(get_db()) as db:
        data = get_recipe_by_id(db, recipe_id)
    
        response = data.__dict__.copy()
        response['categories'] = [cat.name for cat in data.categories]
    return response

def get_sessions() -> list[Session]:
    """
    Serviço para listar todas as sessões.
    :return: Lista de objetos SessionResponseDTO representando as sessões.
    """
    with next(get_db()) as db:
        sessions = get_all_sessions(db)
        return sessions
    
def update_recipe_service(recipe_id: int, dto: RecipeCreateDTO) -> Recipe:
    with next(get_db()) as db:
        recipe = get_recipe_by_id(db, recipe_id)
        recipe.title = dto.title
        recipe.description = dto.description
        recipe.images = [Image(url=image.url) for image in dto.images]
        recipe.session_id = dto.session_id
        recipe.preparation_time = dto.preparation_time
        recipe.dificulty = dto.dificulty
        recipe.portions = dto.portions
        recipe.categories = [
            Category(name=category) for category in dto.categories
        ]
        recipe.ingredients = [
            Ingredient(title=ingredient.title, description=ingredient.description)
            for ingredient in dto.ingredients
        ]
        recipe.preparations = [
            Preparation(title=prep.title, description=prep.description, step=prep.step)
            for prep in dto.preparations
        ]
        db.commit()
        db.refresh(recipe)
        
        ingredients_list = [ing.title for ing in recipe.ingredients]
        ingredients_text = ", ".join(ingredients_list)
        ingredients_keywords = [ing.lower().strip() for ing in ingredients_list]

        doc = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "categories": [cat.name for cat in recipe.categories],
            "images": [img.url for img in recipe.images] if recipe.images else [],
            "preparation_time": recipe.preparation_time,
            "dificulty": recipe.dificulty,
            "portions": recipe.portions,
            "ingredients": ingredients_list,
            "ingredients_text": ingredients_text,
            "ingredients_keywords": ingredients_keywords,
            "preparations": [prep.title for prep in recipe.preparations],
            "session_id": recipe.session_id,
        }

        try:
            index.update_documents([doc])
        except Exception as e:
            print(f"Erro ao atualizar receita {recipe.id} no Meilisearch: {e}")

        return recipe


def delete_recipe_service(recipe_id: int) -> Recipe:
    with next(get_db()) as db:
        recipe = get_recipe_by_id(db, recipe_id)
        db.delete(recipe)
        db.commit()
         # Deletar do Meilisearch
    try:
        index.delete_document(str(recipe_id))  # Se o ID for int, converta para string
    except:
        print(f"Erro ao remover receita {recipe_id} no Meilisearch:")

    return recipe
    
def set_categories_service(recipe_id: int, categories: list[str]) -> Recipe:
    with next(get_db()) as db:
    
        recipe = get_recipe_by_id(db, recipe_id)
        
        # Buscar categorias no banco pelo nome
        categories = db.query(Category).filter(Category.name.in_(categories)).all()
        
        recipe.categories = categories  # Aqui associamos os objetos Category, não strings
        
        db.commit()
        db.refresh(recipe)
            # Atualizar no Meilisearch
    doc = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "categories": [cat.name for cat in recipe.categories],
        "images": [img.url for img in recipe.images] if recipe.images else [],
        "preparation_time": recipe.preparation_time,
        "dificulty": recipe.dificulty,
        "portions": recipe.portions,
        "ingredients": [ing.title for ing in recipe.ingredients],
        "preparations": [prep.title for prep in recipe.preparations],
        "session_id": recipe.session_id,
    }

    try:
        index.update_documents([doc])
    except:
        print(f"Erro ao atualizar categorias da receita {recipe.id} no Meilisearch:")

    return recipe

def filter_recipes_by_categories_service(
    dto:RecipeRequestFilterDTO
) -> list[RecipeListResponseDTO]:
    db = next(get_db())

    # Buscar categorias pelo nome
    categories = db.query(Category).filter(Category.name.in_(categories)).all()

    # Se nenhuma categoria foi encontrada, retorna lista vazia
    if not categories:
        return []

    # Buscar receitas que tenham pelo menos uma das categorias
    query = (
        db.query(Recipe)
        .filter(Recipe.categories.any(Category.id.in_([cat.id for cat in categories])))
        .limit(dto.size)
        .offset((dto.page - 1) * dto.size)
    )

    recipes = query.all()

    return [
        RecipeListResponseDTO(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            tumbnail=recipe.images[0].url if recipe.images else None,
        )
        for recipe in recipes
    ]

def get_all_recipe_service_meilisearch() -> List[RecipeListResponseDTO]:
    db = next(get_db())
    recipes = get_all_recipes(db)
    
    docs_for_index = []
    for recipe in recipes:
        ingredients_list = [ing.description for ing in recipe.ingredients]
        ingredients_text = ", ".join(ingredients_list)
        ingredients_keywords = [ing.lower().strip() for ing in ingredients_list]
        
        doc = {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "categories": [cat.name for cat in recipe.categories],
            "images": [img.url for img in recipe.images] if recipe.images else [],
            "preparation_time": recipe.preparation_time,
            "dificulty": recipe.dificulty,
            "portions": recipe.portions,
            "ingredients": ingredients_list,
            "ingredients_text": ingredients_text,
            "ingredients_keywords": ingredients_keywords,
            "preparations": [prep.title for prep in recipe.preparations],
            "property": recipe.property,
        }
        docs_for_index.append(doc)
    
    try:
        index.add_documents(docs_for_index)
    except Exception as e:
        print(f"Erro ao indexar receitas no Meilisearch: {e}")
    
    return [
        RecipeListResponseDTO(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            tumbnail=recipe.images[0].url if recipe.images else None,
        )
        for recipe in recipes
    ]


def search_recipes_by_categories(dto: RecipeRequestFilterDTO):
    filter_conditions = ['property = "admin"']

    if dto.categories:
        category_filter = " OR ".join([f"categories = '{cat}'" for cat in dto.categories])
        filter_conditions.append(f"({category_filter})")

    filter_expr = " AND ".join(filter_conditions) if filter_conditions else None

    try:
        result = index.search(
            " ".join(dto.ingredients) if dto.ingredients else dto.query,  # 🔹 Busca fuzzy nos ingredientes
            {
                "limit": dto.size,
                "offset": 0,
                "hitsPerPage": dto.size,
                "page": dto.page,
                "filter": filter_expr,
                "attributesToSearchOn": ["ingredients_text"]  # 🔹 Foco na busca dentro dos ingredientes
            }
        )

        if "hits" not in result or not result["hits"]:
            print("Nenhuma receita encontrada.")
            return []

        return {
            "total_pages": result["totalPages"],
            "recipes": [
                RecipeListResponseDTO(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    tumbnail=item["images"][0] if "images" in item else None,
                )
                for item in result["hits"]
            ]
        }
    except Exception as e:
        print(f"Erro ao buscar receitas no Meilisearch: {e}")
        return []

def add_recipe_to_collection_service(collection_id: int, recipe_id: int):
    with next(get_db()) as db:
        collection = get_collection_by_id(db, collection_id)
        recipe = get_recipe_by_id(db, recipe_id)
        collection.recipes.append(recipe)
        db.commit()
        db.refresh(collection)
        return collection
    

def update_recipe_to_session_service(session_id: int, recipe_id: int):
    with next(get_db()) as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        session.recipes.remove(recipe)
        session.recipes.append(recipe)
        db.commit()
        db.refresh(session)
        return session

def ask_order_service(dto: AskRecipeDTO):
    with next(get_db()) as db:
        new_ask_recipe = AskRecipe(description=dto.description)
        db.add(new_ask_recipe)
        db.commit()
        db.refresh(new_ask_recipe)
        return new_ask_recipe