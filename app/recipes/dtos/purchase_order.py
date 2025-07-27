from typing import Optional
from pydantic import BaseModel


class CreatePurchaseOrderDTO(BaseModel):
    product_id: int
    


class PurchaseOrderResponseDTO(BaseModel):
    id: int
    product_id: int
    user_id: int
    created_at: str  # Data de criação do pedido
    last_payment: Optional[str] = None  # Data do último pagamento
    expired_at: Optional[str] = None  # Data de expiração do pedido
    protocol: str

    class Config:
        orm_mode = True