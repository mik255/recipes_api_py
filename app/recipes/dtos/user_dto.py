from pydantic import BaseModel
class UserResponseDTO(BaseModel):
    id: int
    google_id: str
    email: str
    photo_url: str
    name: str
    plan_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True
        
        
class UserSaveRequestDTO(BaseModel):
    google_id: str
    email: str
    photo_url: str
    name: str

    class Config:
        orm_mode = True
        from_attributes = True