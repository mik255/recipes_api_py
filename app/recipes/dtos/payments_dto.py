from pydantic import BaseModel

class payerDto(BaseModel):
    email: str

    class Config:
        orm_mode = True

class CardDto(BaseModel):
    card_number: str
    card_holder_name: str
    card_expiration_date: str
    card_cvv: str
    
    class Config:
        orm_mode = True
        
class CheckoutDto(BaseModel):
    plan_id: str
    description: str

    class Config:
        orm_mode = True