from app.database.dependences import get_db

from app.recipes.dtos.post_dto import PostCreateDTO
from app.recipes.models.post import Post
from app.recipes.repository.posts_repository import create_post, delete_post_by_id, get_all_posts, get_post_by_id, get_posts_by_user_id, get_posts_paginated


def create_post_service(dto: PostCreateDTO, user_id: int):
    with next(get_db()) as db:
        post = Post(
            user_id=user_id,
            description=dto.description,
            recipe_id=dto.recipe_id
        )
        return create_post(db, post)


def list_posts_service():
    with next(get_db()) as db:
        return get_all_posts(db)


def get_post_by_id_service(post_id: int):
    with next(get_db()) as db:
        post = get_post_by_id(db, post_id)
        if post:
            return post
        return False


def delete_post_service(post_id: int):
    with next(get_db()) as db:
        return delete_post_by_id(db, post_id)

def list_posts_service(page: int):
    with next(get_db()) as db:
        return get_posts_paginated(db, page=page, size=10)
    
def get_post_by_user_id_service(user_id: int):
    with next(get_db()) as db:
        post = get_posts_by_user_id(db, user_id)
        if post:
            return post
        return False
