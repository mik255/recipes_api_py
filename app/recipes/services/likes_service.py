from app.database.dependences import get_db
from app.recipes.repository.likes_repository import (
    create_like,
    delete_like,
    count_likes_by_post
)
from app.recipes.models.like import Like

def create_like_service(post_id: int, user_id: int):
    with next(get_db()) as db:
        like = Like(user_id=user_id, post_id=post_id)
        return create_like(db, like)

def delete_like_service(post_id: int, user_id: int):
    with next(get_db()) as db:
        return delete_like(db, post_id, user_id)

def count_likes_by_post_service(post_id: int) -> int:
    with next(get_db()) as db:
        return count_likes_by_post(db, post_id)
