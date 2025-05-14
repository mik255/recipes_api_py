from sqlalchemy.orm import Session
from app.recipes.dtos.contact_dto import ContactMessageDTO
from app.recipes.models.cardapio_digital_leads import ContactMessage

def create_contact(dto: ContactMessageDTO, db: Session):
    message = ContactMessage(**dto.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_all_contacts(db: Session):
    return db.query(ContactMessage).all()
