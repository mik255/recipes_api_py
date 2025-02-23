from app.database.dependences import get_db
from app.recipes.dtos.session_dto import SessionRequestDTO
from app.recipes.models.session import Session
from app.recipes.repository.recipe_repository import get_all_sessions
from app.recipes.repository.session_repository import create_session


def create_session_service(dto: SessionRequestDTO):
    with next(get_db()) as db:
        _session = Session(
            title=dto.title, 
            description=dto.description, 
            type=dto.type, 
            recipeType=dto.recipetype
            )
        return create_session(db, _session)


def get_sessions() -> list[Session]:
    with next(get_db()) as db:
        sessions = get_all_sessions(db)
        return sessions