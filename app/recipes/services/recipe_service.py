from app.database.dependences import get_db
from app.recipes.dtos.recipe_dto import RecipeCreateDTO, RecipeListResponseDTO
from app.recipes.dtos.session_dto import SessionResponseDTO
from app.recipes.models.recipe import Recipe
from app.recipes.models.ingredient import Ingredient
from app.recipes.models.preparation import Preparation
from app.recipes.models.image import Image
from app.recipes.models.session import Session
from app.recipes.repository.recipe_repository import get_all_recipes, get_recipe_by_id, get_all_sessions


def create_recipe_service(recipe_dto: RecipeCreateDTO) -> Recipe:
    """
    Serviço para criar uma nova receita.
    :param recipe_dto: Objeto de entrada do tipo RecipeCreateDTO contendo os dados da receita.
    :return: Objeto Recipe criado no banco de dados.
    """
    with next(get_db()) as db:
        # Criar a instância do modelo Recipe
        new_recipe = Recipe(title=recipe_dto.title)

        # Adicionar imagens
        new_recipe.images = [Image(url=image.url) for image in recipe_dto.images]

        # Adicionar ingredientes
        new_recipe.ingredients = [
            Ingredient(title=ingredient.title, quantity=ingredient.quantity)
            for ingredient in recipe_dto.ingredients
        ]

        # Adicionar modos de preparo
        new_recipe.preparations = [
            Preparation(title=prep.title, description=prep.description)
            for prep in recipe_dto.preparations
        ]

        # Persistir no banco de dados via repositório
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

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
                description=None,
                tumbnail=recipe.images[0].url if recipe.images else None,
            )
            for recipe in recipes
        ]


def get_recipe_by_id_service(recipe_id: int) -> Recipe:
    """
    Serviço para buscar uma receita pelo ID.
    :param recipe_id: ID da receita a ser buscada.
    :return: Objeto Recipe correspondente ao ID fornecido.
    """
    with next(get_db()) as db:
        return get_recipe_by_id(db, recipe_id)


def get_sessions() -> list[Session]:
    """
    Serviço para listar todas as sessões.
    :return: Lista de objetos SessionResponseDTO representando as sessões.
    """
    with next(get_db()) as db:
        sessions = get_all_sessions(db)
        return sessions