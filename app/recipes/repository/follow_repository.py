from sqlalchemy.orm import Session
from app.recipes.models.follow import Follow
from app.recipes.models.user import User

def create_follow(db: Session, follower_id: int, following_id: int):
    follow = Follow(follower_id=follower_id, following_id=following_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def delete_follow(db: Session, follower_id: int, following_id: int):
    follow = db.query(Follow).filter_by(follower_id=follower_id, following_id=following_id).first()
    if not follow:
        raise Exception("Relação de follow não encontrada")
    db.delete(follow)
    db.commit()

def get_followers(db: Session, user_id: int):
    return (
        db.query(Follow)
        .join(User, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
        .all()
    )

def get_following(db: Session, user_id: int):
    return (
        db.query(Follow)
        .join(User, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
        .all()
    )
