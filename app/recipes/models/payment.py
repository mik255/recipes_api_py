


from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.config import Base

class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))  # Chave estrangeira para o Order
    amount = Column(Integer, index=False)
    method = Column(String, nullable=False)  # Método de pagamento utilizado no pedido
    status = Column(String, default="pending")  # Status do pedido (pending, paid, expired)
    getway_payment_id = Column(BigInteger, nullable=True)  # ID do pagamento
    order = relationship("Order", back_populates="payments")
    # Campos de data
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação do pedido


