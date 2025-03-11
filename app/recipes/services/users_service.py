from app.database.dependences import get_db
from app.recipes.dtos.user_dto import UserSaveRequestDTO
from app.recipes.models.user import User
from app.recipes.repository.user_repository import create_user


def create_user_service(dto: UserSaveRequestDTO):
    with next(get_db()) as db:
        _user = User(
            name=dto.name, 
            email=dto.email, 
            google_id=dto.google_id,
            photo_url=dto.photo_url
            )
        return create_user(db, _user)

def verify_user_exists(google_id: str):
    with next(get_db()) as db:
        user = db.query(User).filter(User.google_id == google_id).first()
        if user:
            return user
        return False