from sqlalchemy.orm import Session
from app.recipes.models.collection import Collection
from app.recipes.models.user import User
def create_collection(db: Session, collection: Collection):
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

def get_all(db: Session):
    return db.query(Collection).all()

def get_collections_by_user_id(db: Session, google_id: str):
    user = db.query(User).filter(User.google_id == google_id).first()
    if user:
        return user.collections
    return []

def get_recipes_collection(db: Session, collection_id: int):
    return db.query(Collection).filter(Collection.id == collection_id).first().recipes
