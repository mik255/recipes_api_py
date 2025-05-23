from fastapi import HTTPException
from app.database.dependences import get_db
from app.recipes.dtos.session_dto import SessionRequestDTO
from app.recipes.models.session import Session
from app.recipes.repository.recipe_repository import get_all_sessions
from app.recipes.repository.session_repository import create_session,add_recipe_to_session


def create_session_service(dto: SessionRequestDTO):
    with next(get_db()) as db:
        _session = Session(
            title=dto.title, 
            description=dto.description, 
            type=dto.type, 
            recipeType=dto.recipe_type
            )
        return create_session(db, _session)

def get_recipes_by_session(session_id: int, size: int = 0, limit: int = 5):
    with next(get_db()) as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        return session.recipes[:limit]
    
def get_recipes_by_session_id(session_id: int):
    with next(get_db()) as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        if session is None:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")

        return {
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "type": session.type,
            "recipetype": session.recipeType,
            "recipes": [
                {
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description,
                    "tumbnail": recipe.images[0].url if recipe.images else None,
                    "preparation_time": int(recipe.preparation_time) if recipe.preparation_time is not None else 0
                    
                    # adicione mais campos aqui se quiser
                }
                for recipe in session.recipes
            ],
        }

def get_sessions() -> list[Session]:
    with next(get_db()) as db:
        sessions = get_all_sessions(db)
        return sessions

def add_recipe_to_session_service(session_id: int, recipe_id: int):
    with next(get_db()) as db:
        return add_recipe_to_session(db, session_id, recipe_id)
    
def update_session_service(session_id: int, dto: SessionRequestDTO):
    with next(get_db()) as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        session.title = dto.title
        session.description = dto.description
        session.type = dto.type
        session.recipeType = dto.recipe_type
        db.commit()
        db.refresh(session)
        return
    