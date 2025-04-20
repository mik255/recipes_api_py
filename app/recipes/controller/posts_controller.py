from fastapi import APIRouter, HTTPException
from typing import List
from fastapi import APIRouter, Header,HTTPException, Depends, Query

from app.recipes.dtos.post_dto import PaginedPostResponseDTO, PostCreateDTO, PostResponseDTO
from app.recipes.services.posts_service import create_post_service, delete_post_service, get_post_by_id_service, get_post_by_user_id_service, list_posts_service


router = APIRouter()

@router.post("/", response_model=PostResponseDTO, status_code=201)
def create_post_route(dto: PostCreateDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:
        return create_post_service(dto, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{page}", response_model=PaginedPostResponseDTO)
def list_posts_route(page: int):
    try:
        return list_posts_service(page=page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{post_id}", response_model=PostResponseDTO)
def get_post_by_id_route(post_id: int):
    try:
        return get_post_by_id_service(post_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{post_id}", status_code=204)
def delete_post_route(post_id: int):
    try:
        delete_post_service(post_id)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[PostResponseDTO])
def list_posts(skip: int = 0, limit: int = 10):
    try:
        return list_posts_service(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
@router.get("/user/all", response_model=List[PostResponseDTO])
def get_post_by_user_id_route(user_id: int = Header(..., alias="X-User-Id")):
    try:
        return get_post_by_user_id_service(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

