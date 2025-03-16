from sqlalchemy.orm import Session
from app.recipes.models.session import Session as SessionModel
from app.recipes.models.recipe import Recipe

def create_recipe(db: Session, recipe: Recipe):
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_all_recipes(db: Session):
    return db.query(Recipe).all()

def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def get_all_sessions(db: Session):
    return db.query(SessionModel).filter(SessionModel.id != 5).all()