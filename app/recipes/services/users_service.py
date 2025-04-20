from sqlalchemy import func
from app.database.dependences import get_db
from app.recipes.dtos.user_dto import UserResponseDTO, UserSaveRequestDTO
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
    
def get_user_by_id(user_id: int):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
        return False
    
def get_creators_service():
    with next(get_db()) as db:
        users = db.query(User).filter(User.creator_nick_name.isnot(None)).limit(10).all()  # Filtra e limita a 10 usuários
        if users:
            return users
        return []
    
def post_creators_service(dto: UserResponseDTO):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == dto.user_id).first()
        if user:
            user.creator_nick_name = dto.creator_nick_name
            user.creator_start_at = func.now()
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        return False
    
def get_user_by_id_service(user_id: int):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
        return False