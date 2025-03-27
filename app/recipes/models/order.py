from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.config import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plan.id"))
    user_id = Column(Integer, ForeignKey("user.id"))  # Chave estrangeira para o User
    plan = relationship("Plan", back_populates="orders")
    amount = Column(Float, index=False)

    # Campos de data
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação do pedido
    last_payment = Column(DateTime, nullable=False)  # Data do último pagamento
    expired_at = Column(DateTime, nullable=False)  # Data de expiração do pedido
    status = Column(String, default="pending")  # Status do pedido (pending, paid, expired)
    payment_method = Column(String, nullable=False)  # Método de pagamento utilizado no pedido
    payment_id = Column(String, nullable=False)  # ID do pagamento