from app.database.dependences import get_db
from app.recipes.dtos.comment_dto import CommentCreateDTO
from app.recipes.models.comments import Comment
from app.recipes.repository.comments_repository import (
    create_comment,
    list_comments_by_post,
    delete_comment
)

def create_comment_service(dto: CommentCreateDTO, user_id: int):
    with next(get_db()) as db:
        comment = Comment(
            text=dto.text,
            user_id=user_id,
            post_id=dto.post_id,
        )
        return create_comment(db, comment)

def list_comments_by_post_service(post_id: int, skip: int = 0, limit: int = 10):
    with next(get_db()) as db:
        return list_comments_by_post(db, post_id, skip, limit)

def delete_comment_service(comment_id: int):
    with next(get_db()) as db:
        return delete_comment(db, comment_id)
