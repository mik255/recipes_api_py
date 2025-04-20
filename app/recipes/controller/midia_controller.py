from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.dependences import get_db
from app.recipes.dtos.midia_dto import MediaResponseDTO, MediaSaveRequestDTO
from app.recipes.services.midia_service import create_media_service, delete_media_service, get_all_media, get_media_by_id, update_media_service  # Dependência para obter a sessão do banco de dados

# Inicializa o roteador para o módulo de mídia
router = APIRouter()

# Rota para criar uma nova mídia
@router.post("/", response_model=MediaResponseDTO, status_code=201)
def create_media(dto: MediaSaveRequestDTO, db: Session = Depends(get_db)):
    try:
        return create_media_service(dto, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Rota para obter todas as mídias
@router.get("/", response_model=List[MediaResponseDTO])
def get_media(db: Session = Depends(get_db)):
    try:
        return get_all_media(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Rota para obter uma mídia específica pelo ID
@router.get("/{media_id}", response_model=MediaResponseDTO)
def get_media_by_id_route(media_id: int, db: Session = Depends(get_db)):
    try:
        return get_media_by_id(media_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Rota para atualizar uma mídia
@router.put("/{media_id}", response_model=MediaResponseDTO)
def update_media(media_id: int, dto: MediaSaveRequestDTO, db: Session = Depends(get_db)):
    try:
        return update_media_service(media_id, dto, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Rota para excluir uma mídia
@router.delete("/{media_id}", status_code=204)
def delete_media(media_id: int, db: Session = Depends(get_db)):
    try:
        return delete_media_service(media_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
