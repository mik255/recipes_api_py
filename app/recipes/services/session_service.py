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
    