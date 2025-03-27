from sqlalchemy.orm import Session
from app.recipes.models.session import Session as SessionModel
from app.recipes.models.recipe import Recipe
from sqlalchemy.orm import Session, selectinload
def create_session(db: Session, model: SessionModel):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def get_all_sessions(db: Session):
    return (
        db.query(SessionModel)
        .options(
            selectinload(SessionModel.recipes)
                .load_only(
                    Recipe.id,
                    Recipe.title,
                    Recipe.description,
                    Recipe.tumbnail,
                    Recipe.property
                )
        )
        .all()
    )

def add_recipe_to_session(db: Session, session_id: int, recipe_id: int):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    session.recipes.append(recipe)
    db.commit()
    db.refresh(session)
    return session