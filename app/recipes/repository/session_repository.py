from sqlalchemy.orm import Session
from app.recipes.models.session import Session as SessionModel
from app.recipes.models.recipe import Recipe

def create_session(db: Session, model: SessionModel):
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def get_all_sessions(db: Session):
    return db.query(SessionModel).all()