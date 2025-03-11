from sqlalchemy.orm import Session
from app.recipes.models.session import Session as SessionModel
from app.recipes.models.user import User

def create_user(db: Session, model: User):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
