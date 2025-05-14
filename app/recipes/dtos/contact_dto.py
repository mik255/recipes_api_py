from pydantic import BaseModel

class ContactMessageDTO(BaseModel):
    nome: str
    email: str
    telefone: str
    restaurante: str
    mensagem: str


class ContactMessageResponseDTO(ContactMessageDTO):
    id: int

    class Config:
        orm_mode = True