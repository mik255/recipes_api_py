from pydantic import BaseModel
from typing import Optional

class FollowBaseDTO(BaseModel):
    follower_id: int
    following_id: int

class FollowCreateDTO(FollowBaseDTO):
    pass

class FollowResponseDTO(BaseModel):
    id: Optional[int] = None
    follower_id: int
    following_id: int

    class Config:
        orm_mode = True
