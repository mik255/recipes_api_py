from requests import Session
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.recipes.dtos.product_dto import ProductResponseDTO
from app.recipes.dtos.purchase_order import CreatePurchaseOrderDTO
from app.recipes.models.product import Product
from app.recipes.models.user import User
from app.recipes.models.purchase_order import PurchaseOrder
from datetime import datetime, timedelta


def create_purchase_order_repository(
    db: Session, 
    dto: CreatePurchaseOrderDTO, 
    user: User,
    protocol: str
):
    product: Product = db.query(Product).filter(Product.id == dto.product_id).first()
    
    if not product:
        raise ValueError("Product not found")

    now = datetime.utcnow()

    purchase_order = PurchaseOrder(
        product_id=product.id,
        user_id=user.id,
        protocol=protocol,
        last_payment=now,
        expired_at=now + timedelta(days=product.delta_expiration_in_days)
    )

    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)

    return purchase_order
