import os
import boto3
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from app.recipes.dtos.ask_recipe_dto import AskRecipeDTO
from app.recipes.dtos.image_dto import ImageDTO
from app.recipes.dtos.recipe_dto import (
    IARecipeCreateDTO,
    RecipeCreateDTO,
    RecipeListResponseDTO,
    RecipeRequestFilterDTO,
    RecipeResponseDTO,
)
from app.recipes.services.IA.create_recipe import IA_recipe_creator
from app.recipes.services.recipe_service import (
    add_recipe_to_collection_service,
    create_recipe_service,
    get_all_recipe_service,
    get_all_recipe_service_meilisearch,
    get_recipe_by_id_service,
    search_recipes_by_categories,
    update_recipe_service,
    delete_recipe_service,
    set_categories_service,
    ask_order_service,
)
from app.recipes.services.session_service import (
    add_recipe_to_session_service,
)

# Configuração do Bucket S3
AWS_ACCESS_KEY = os.getenv("IAM_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("IAM_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = "sa-east-1"  # Exemplo para São Paulo

# Instanciando cliente S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

router = APIRouter()

# 🔹 Endpoint separado para fazer upload da imagem para o S3
# 🔹 Endpoint para fazer upload da imagem para o S3
@router.post("/save-image", response_model=ImageDTO, status_code=201)
async def upload_image_to_s3(image: UploadFile = File(...)) -> ImageDTO:
    try:
        file_extension = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # ✅ Remove "ACL: public-read"
        s3_client.upload_fileobj(
            image.file,
            AWS_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": image.content_type}  # Mantendo apenas ContentType
        )

        image_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        return ImageDTO(url=image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da imagem para o S3: {str(e)}")
    # Rota para criar um novo REcipe
@router.post("/", response_model=RecipeResponseDTO, status_code=201)
def create_recipe_route(dto: RecipeCreateDTO):

    try:
        recipe = create_recipe_service(dto)
        if dto.collection_id:
            add_recipe_to_collection_service(recipe_id=recipe.id, collection_id =dto.collection_id)
        add_recipe_to_session_service(session_id=dto.session_id, recipe_id=recipe.id)
        set_categories_service(recipe.id, dto.categories)
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/ia_recipe_creator", response_model=RecipeResponseDTO, status_code=201)
def IA_recipe_creator_route(dto: IARecipeCreateDTO):

    try:
        recipe = IA_recipe_creator(dto.title,dto.session_id)
        add_recipe_to_session_service(session_id=dto.session_id, recipe_id=recipe.id)
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", response_model=List[RecipeListResponseDTO], status_code=200)
def list_recipe_route():
    try:
        return get_all_recipe_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/filter", response_model=List[RecipeListResponseDTO], status_code=200)
def list_recipe_route(dto:RecipeRequestFilterDTO):
    try:
        return search_recipes_by_categories(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.get("/{recipe_id}", response_model=RecipeResponseDTO, status_code=200)
def get_recipe_by_id_route(recipe_id: int):
    try:
        data = get_recipe_by_id_service(recipe_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.put("/{recipe_id}", response_model=RecipeResponseDTO, status_code=200)
def update_recipe_route(recipe_id: int, dto: RecipeCreateDTO):
    try:
        return update_recipe_service(recipe_id, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
# deletar
@router.delete("/{recipe_id}", status_code=204)
def delete_recipe_route(recipe_id: int):
    try:
        return delete_recipe_service(recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/meilisearch", status_code=200)
def delete_recipe_route():
    try:
        return get_all_recipe_service_meilisearch()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/ask_order", status_code=200)
def ask_order_route(dto:AskRecipeDTO):
    try:
        return ask_order_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")