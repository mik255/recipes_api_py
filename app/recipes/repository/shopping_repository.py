
from sqlalchemy.orm import selectinload

from app.recipes.models.ingredient import Ingredient


def get_lists_by_user_id(db, user_id: int):
    results = (
        db.query(Ingredient)
        .options(
            selectinload(Ingredient.recipe),
            selectinload(Ingredient.shopping_items),
        )
        .filter(Ingredient.user_id == user_id)
        .all()
    )
    return results

def get_list_by_id(db, list_id: int):
    results = (
        db.query(ShoppingList)
        .options(
            selectinload(ShoppingList.user),
            selectinload(ShoppingList.recipe),
            selectinload(ShoppingList.shopping_items),
        )
        .filter(ShoppingList.id == list_id)
        .first()
    )
    return results

def create_list(db, list_obj):
    db.add(list_obj)
    db.commit()
    db.refresh(list_obj)
    return list_obj

def update_list(db, list_obj):
    db.commit()
    db.refresh(list_obj)
    return list_obj

def delete_list(db, list_obj):
    db.delete(list_obj)
    db.commit()
    return list_obj

