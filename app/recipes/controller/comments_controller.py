from fastapi import APIRouter, HTTPException, Header
from typing import List
from app.recipes.dtos.comment_dto import CommentCreateDTO, CommentResponseDTO
from app.recipes.services.comments_service import (
    create_comment_service,
    delete_comment_service,
    list_comments_by_post_service
)

router = APIRouter()

@router.post("/", response_model=CommentResponseDTO, status_code=201)
def create_comment(dto: CommentCreateDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:
        return create_comment_service(dto,user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar comentário: {str(e)}")

@router.get("/post/{post_id}", response_model=List[CommentResponseDTO])
def list_comments_by_post(post_id: int, skip: int = 0, limit: int = 10):
    try:
        return list_comments_by_post_service(post_id, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar comentários: {str(e)}")

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int):
    try:
        delete_comment_service(comment_id)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Comentário não encontrado: {str(e)}")
