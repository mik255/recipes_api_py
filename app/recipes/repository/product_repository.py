from requests import Session
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.recipes.dtos.product_dto import ProductResponseDTO
from app.recipes.models.product import Product
from app.recipes.models.recipe import Recipe


def get_all_recipes_products(db: Session):
    results = (
        db.query(Product)
        .options(
            selectinload(Product.recipes)
        )
        .order_by(Product.id)
        .all()
    )

    return [ProductResponseDTO.from_orm(product) for product in results]

def add_recipe_to_product_repository(db: Session, *args, **kwargs):
    dto = args[0]  # Extrai o DTO da tupla
    product_id = dto.product_id
    recipe_id = dto.recipe_id

    product: Product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"error": "Product not found"}

    recipe: Recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        return {"error": "Recipe not found"}

    product.recipes.append(recipe)
    db.commit()
    db.refresh(product)

    return {"message": "Recipe added to product successfully"}
 
