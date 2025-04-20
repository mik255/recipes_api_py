from sqlalchemy.orm import Session
from app.recipes.models.like import Like


def create_like(db: Session, like: Like):
    existing = db.query(Like).filter_by(user_id=like.user_id, post_id=like.post_id).first()
    if existing:
        raise Exception("Usuário já curtiu este post")
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def delete_like(db: Session, post_id: int, user_id: int):
    like = db.query(Like).filter_by(post_id=post_id, user_id=user_id).first()
    if not like:
        raise Exception("Like não encontrado")
    db.delete(like)
    db.commit()
    return True


def count_likes_by_post(db: Session, post_id: int) -> int:
    return db.query(Like).filter_by(post_id=post_id).count()
