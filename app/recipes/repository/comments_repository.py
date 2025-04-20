from sqlalchemy.orm import Session

from app.recipes.models.comments import Comment


def create_comment(db: Session, comment: Comment):
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise Exception("Comentário não encontrado")
    db.delete(comment)
    db.commit()
