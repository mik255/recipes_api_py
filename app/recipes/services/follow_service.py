from app.database.dependences import get_db
from app.recipes.models.follow import Follow
from app.recipes.repository.follow_repository import (
    create_follow,
    delete_follow,
    get_followers,
    get_following,
)

def follow_user_service(follower_id: int, following_id: int):
    if follower_id == following_id:
        raise Exception("Você não pode seguir a si mesmo.")
    with next(get_db()) as db:
        return create_follow(db, follower_id, following_id)

def unfollow_user_service(follower_id: int, following_id: int):
    with next(get_db()) as db:
        return delete_follow(db, follower_id, following_id)

def get_followers_service(user_id: int):
    with next(get_db()) as db:
        return get_followers(db, user_id)

def get_following_service(user_id: int):
    with next(get_db()) as db:
        return get_following(db, user_id)
