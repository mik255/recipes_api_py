from fastapi import APIRouter, Header,HTTPException, Depends, Query
from typing import List

from app.recipes.dtos.product_dto import AddRecipeToProductDTO, ProductResponseDTO
from app.recipes.services.product_service import list_products_service
from app.recipes.services.purchase_order_service import add_recipe_to_product_service, get_product_by_id_service


router = APIRouter()


    
@router.get("/", response_model=List[ProductResponseDTO], status_code=200)
def get_recipe_by_id_route():
    try:
        return list_products_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/add-recipe", status_code=201)
def add_recipe_to_product_route(dto: AddRecipeToProductDTO):
    try:
        return add_recipe_to_product_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/get-product-by-id", response_model=ProductResponseDTO, status_code=200)
def get_product_by_id_route(dto: dict):
    try:
        return get_product_by_id_service(dto.get("product_id"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
