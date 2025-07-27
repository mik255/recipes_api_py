
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.config import Base
from datetime import datetime

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="purchase_orders")
    user_id = Column(Integer, ForeignKey("user.id"))  # Chave estrangeira para o User
    user = relationship("User", back_populates="purchase_orders")    # Campos de data
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação do pedido
    last_payment = Column(DateTime, nullable=True)  # Data do último pagamento
    expired_at = Column(DateTime, nullable=True,default=datetime.utcnow) # Data de expiração do pedido
    protocol = Column(String, nullable=False)
    