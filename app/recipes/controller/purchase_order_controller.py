from fastapi import APIRouter, Header,HTTPException, Depends, Query
from typing import List

from app.recipes.dtos.purchase_order import CreatePurchaseOrderDTO
from app.recipes.services.purchase_order_service import create_purchase_order_service, get_purchase_orders_service


router = APIRouter()

@router.post("/", status_code=201)
def create_recipe_route(dto: CreatePurchaseOrderDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:
        return create_purchase_order_service(dto, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", status_code=200)
def get_purchase_orders_route(user_id: int = Header(..., alias="X-User-Id")):
    try:
        return get_purchase_orders_service(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    