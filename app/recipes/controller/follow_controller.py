from fastapi import APIRouter, HTTPException
from typing import List
from app.recipes.services.follow_service import (
    follow_user_service,
    unfollow_user_service,
    get_followers_service,
    get_following_service,
)
from app.recipes.dtos.follow_dto import FollowResponseDTO

router = APIRouter(prefix="/follow", tags=["Follow"])

@router.post("/{follower_id}/follow/{following_id}", status_code=201)
def follow_user(follower_id: int, following_id: int):
    try:
        return follow_user_service(follower_id, following_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{follower_id}/unfollow/{following_id}", status_code=204)
def unfollow_user(follower_id: int, following_id: int):
    try:
        unfollow_user_service(follower_id, following_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/followers", response_model=List[FollowResponseDTO])
def get_followers(user_id: int):
    try:
        return get_followers_service(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
