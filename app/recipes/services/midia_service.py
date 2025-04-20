from sqlalchemy.orm import Session
from app.recipes.dtos.midia_dto import MediaSaveRequestDTO, MediaResponseDTO
from fastapi import HTTPException

from app.recipes.repository.midia_repository import MidiaRepository

# Função de serviço para criar uma nova mídia
def create_media_service(dto: MediaSaveRequestDTO, db: Session) -> MediaResponseDTO:
    try:
        # Cria a mídia usando os dados fornecidos
        midia = MidiaRepository.create(db=db, url=dto.url, type=dto.type.value)
        # Retorna a resposta da mídia criada
        return MediaResponseDTO(id=midia.id, url=midia.url, type=midia.type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mídia: {str(e)}")

# Função de serviço para obter todas as mídias
def get_all_media(db: Session) -> list[MediaResponseDTO]:
    try:
        midias = MidiaRepository.get_all(db=db)
        # Mapeia as mídias para o DTO de resposta
        return [MediaResponseDTO(id=midia.id, url=midia.url, type=midia.type, post_id=midia.post_id) for midia in midias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter as mídias: {str(e)}")

# Função de serviço para obter uma mídia específica por ID
def get_media_by_id(media_id: int, db: Session) -> MediaResponseDTO:
    try:
        midia = MidiaRepository.get_by_id(db=db, midia_id=media_id)
        if not midia:
            raise HTTPException(status_code=404, detail="Mídia não encontrada")
        return MediaResponseDTO(id=midia.id, url=midia.url, type=midia.type, post_id=midia.post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter a mídia: {str(e)}")

# Função de serviço para atualizar uma mídia
def update_media_service(media_id: int, dto: MediaSaveRequestDTO, db: Session) -> MediaResponseDTO:
    try:
        updated_midia = MidiaRepository.update(db=db, midia_id=media_id, url=dto.url, type=dto.type)
        if not updated_midia:
            raise HTTPException(status_code=404, detail="Mídia não encontrada para atualizar")
        return MediaResponseDTO(id=updated_midia.id, url=updated_midia.url, type=updated_midia.type, post_id=updated_midia.post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar a mídia: {str(e)}")

# Função de serviço para excluir uma mídia
def delete_media_service(media_id: int, db: Session) -> None:
    try:
        deleted_midia = MidiaRepository.delete(db=db, midia_id=media_id)
        if not deleted_midia:
            raise HTTPException(status_code=404, detail="Mídia não encontrada para exclusão")
        return None  # Retorna nada porque é um status 204 (sem conteúdo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir a mídia: {str(e)}")
