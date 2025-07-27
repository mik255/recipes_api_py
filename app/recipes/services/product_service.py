from app.database.dependences import get_db
from app.recipes.repository.product_repository import get_all_recipes_products



def list_products_service():
    with next(get_db()) as db:
        return get_all_recipes_products(db)
