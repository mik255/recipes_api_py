from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.dependences import get_db
from app.recipes.models.cardapio_count import ClickCounter
from app.recipes.dtos.contact_dto import ContactMessageDTO, ContactMessageResponseDTO
from app.recipes.services.contact_service import create_contact, get_all_contacts


router = APIRouter()

@router.post("/lead", response_model=ContactMessageResponseDTO, status_code=201)
def create_contact_route(dto: ContactMessageDTO, db: Session = Depends(get_db)):
    try:
        return create_contact(dto, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/click")
def track_click(db: Session = Depends(get_db)):
    try:
        counter = db.query(ClickCounter).first()
        if not counter:
            counter = ClickCounter(count=1)
            db.add(counter)
        else:
            counter.count += 1
        db.commit()
        db.refresh(counter)
        return {"total_clicks": counter.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar clique: {str(e)}")
