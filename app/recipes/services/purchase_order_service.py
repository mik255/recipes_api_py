
from datetime import datetime
from app.database.dependences import get_db
from app.recipes.dtos.product_dto import ProductResponseDTO
from app.recipes.dtos.purchase_order import CreatePurchaseOrderDTO
from app.recipes.dtos.recipe_dto import RecipeResponseDTO
from app.recipes.models.product import Product
from app.recipes.models.purchase_order import PurchaseOrder
from app.recipes.models.user import User
from app.recipes.repository.product_repository import add_recipe_to_product_repository
from app.recipes.repository.purchase_order_repository import create_purchase_order_repository



def create_purchase_order_service(dto: CreatePurchaseOrderDTO, user_id: int):
    with next(get_db()) as db:
        user = db.query(User).filter(User.id == user_id).first()
        timeStemp = int(datetime.utcnow().timestamp())
        #generate protocol
        protocol = f"PO-{user_id}-{dto.product_id}-{timeStemp}"
        return create_purchase_order_repository(db,dto,user,protocol)

def add_recipe_to_product_service(*args, **kwargs):
    with next(get_db()) as db:
        return add_recipe_to_product_repository(db, *args, **kwargs)
    
def get_purchase_orders_service(user_id: int):
    with next(get_db()) as db:
        return db.query(PurchaseOrder).filter(PurchaseOrder.user_id == user_id).all()

def get_product_by_id_service(product_id: int):
    db = next(get_db())
    try:
        product = db.query(Product).filter_by(id=product_id).first()
        if not product:
            raise ValueError("Product not found")
        return ProductResponseDTO.from_orm(product)

    finally:
        db.close()
