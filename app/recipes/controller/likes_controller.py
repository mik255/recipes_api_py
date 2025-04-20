from fastapi import APIRouter, HTTPException, Header
from app.recipes.dtos.likes_dto import LikeCreateDTO
from app.recipes.services.likes_service import (
    create_like_service,
    delete_like_service,
    count_likes_by_post_service
)

router = APIRouter()

@router.post("/", status_code=201)
def create_like(dto: LikeCreateDTO, user_id: int = Header(..., alias="X-User-Id")):
    try:
        return create_like_service(dto.post_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}", status_code=204)
def delete_like(post_id: int, user_id: int = Header(..., alias="X-User-Id")):
    try:
        delete_like_service(post_id, user_id)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/count/{post_id}")
def count_likes(post_id: int):
    try:
        return {"post_id": post_id, "likes": count_likes_by_post_service(post_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
