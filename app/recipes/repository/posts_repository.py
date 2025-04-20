from requests import Session
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.recipes.dtos.post_dto import PostResponseDTO
from app.recipes.models.comments import Comment
from app.recipes.models.like import Like
from app.recipes.models.post import Post

# Subqueries globais para evitar duplicação
def _get_like_count_subq():
    return (
        select(Like.post_id, func.count(Like.id).label("like_count"))
        .group_by(Like.post_id)
        .subquery()
    )

def _get_comment_count_subq():
    return (
        select(Comment.post_id, func.count(Comment.id).label("comment_count"))
        .group_by(Comment.post_id)
        .subquery()
    )

def _build_post_response(post_obj, likes, comments):
    return {
        "id": post_obj.id,
        "user": post_obj.user,
        "recipe": post_obj.recipe,
        "description": post_obj.description,
        "created_at": post_obj.created_at,
        "likes": likes,
        "comments": comments
    }

# ✅ Create post
def create_post(db: Session, post: Post):
    db.add(post)
    db.commit()
    db.refresh(post)

    post_with_relations = (
        db.query(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.recipe),
        )
        .filter(Post.id == post.id)
        .first()
    )

    return _build_post_response(post_with_relations, [], [])


# ✅ Get all posts (com preload e contadores)
def get_all_posts(db: Session):
    like_count_subq = _get_like_count_subq()
    comment_count_subq = _get_comment_count_subq()

    results = (
        db.query(Post, like_count_subq.c.like_count, comment_count_subq.c.comment_count)
        .outerjoin(like_count_subq, Post.id == like_count_subq.c.post_id)
        .outerjoin(comment_count_subq, Post.id == comment_count_subq.c.post_id)
        .options(
            selectinload(Post.user),
            selectinload(Post.recipe),
        )
        .order_by(Post.created_at.desc())  # <-- aqui garante que os mais recentes vêm primeiro
        .all()
    )

    return [
        _build_post_response(post, like_count, comment_count)
        for post, like_count, comment_count in results
    ]

# ✅ Get single post by ID (com preload e contadores)
def get_post_by_id(db, post_id: int):
    like_count_subq = _get_like_count_subq()
    comment_count_subq = _get_comment_count_subq()

    result = (
        db.query(Post, like_count_subq.c.like_count, comment_count_subq.c.comment_count)
        .outerjoin(like_count_subq, Post.id == like_count_subq.c.post_id)
        .outerjoin(comment_count_subq, Post.id == comment_count_subq.c.post_id)
        .options(
            selectinload(Post.user),
            selectinload(Post.recipe),
        )
        .filter(Post.id == post_id)
        .first()
    )

    if result:
        post_obj, like_count, comment_count = result
        return _build_post_response(post_obj, like_count, comment_count)
    return None

# ✅ Delete post (sem alterações aqui)
def delete_post_by_id(db, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

def get_posts_paginated(db, page: int = 0, size: int = 10):
    offset = page * size

    total = db.query(Post).count()

    results = (
        db.query(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.recipe),
            selectinload(Post.likes),
            selectinload(Post.comments),
        )
        .order_by(Post.created_at.desc())  # ⬅️ Ordena por mais recente
        .offset(offset)
        .limit(size)
        .all()
    )

    posts = [
        _build_post_response_with_lists(post)
        for post in results
    ]

    return {
        "posts": posts,
        "total": total,
        "page": page,
        "size": size
    }


def _build_post_response_with_lists(post_obj):
    return {
        "id": post_obj.id,
        "user": post_obj.user,
        "recipe": post_obj.recipe,
        "description": post_obj.description,
        "created_at": post_obj.created_at,
        "likes": post_obj.likes,  # Lista de likes
        "comments": post_obj.comments  # Lista de comentários
    }
    
def get_posts_by_user_id(db, user_id: int):
    results = (
        db.query(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.recipe),
            selectinload(Post.likes),
            selectinload(Post.comments),
        )
        .filter(Post.user_id == user_id)
        .all()
    )

    posts = [
        _build_post_response_with_lists(post)
        for post in results
    ]

    return posts
