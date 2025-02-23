

from pydantic import BaseModel

class CollectionDTO(BaseModel):
    name: str
    description: str
    icon_name: str
    user_id: int

    class Config:
        orm_mode = True
        

class CollectionResponseDTO(BaseModel):
    id: int
    name: str
    description: str
    icon_name: str

    class Config:
        orm_mode = True
        
        
