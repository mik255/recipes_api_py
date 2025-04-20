
from pydantic import BaseModel

class LikeBaseDTO(BaseModel):
    post_id: int

class LikeCreateDTO(LikeBaseDTO):
    pass

class LikeResponseDTO(LikeBaseDTO):
    class Config:
        orm_mode = True
