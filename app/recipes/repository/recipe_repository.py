from sqlalchemy import select
from sqlalchemy.orm import Session
from app.recipes.models.image import Image
from app.recipes.models.session import Session as SessionModel
from app.recipes.models.recipe import Recipe
from sqlalchemy.orm import Session, selectinload, load_only, joinedload

def create_recipe(db: Session, recipe: Recipe):
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_all_recipes(db: Session):
    stmt = select(Recipe).options(selectinload(Recipe.ingredients))
    return db.scalars(stmt).unique().all()

def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()



def get_all_sessions(db: Session):
    sessions = (
        db.query(SessionModel)
        .options(
            selectinload(SessionModel.recipes)
            .options(
                load_only(
                    Recipe.id,
                    Recipe.title,
                    Recipe.description,
                    Recipe.property,
                ),
                selectinload(Recipe.images).load_only(Image.url),
            )
        )
        .all()
    )

    for session in sessions:
        # Limita em memória após carregamento otimizado
        session.recipes = session.recipes[:10]

    return sessions
