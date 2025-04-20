from io import BytesIO
import os
from PIL import Image as PILImage, UnidentifiedImageError
import uuid
import requests
import boto3
from fastapi import APIRouter, Form, HTTPException, Header, UploadFile, File
from typing import List
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
from app.recipes.services.IA.generate_macro import popular_macros_para_todas_as_receitas
from app.recipes.services.collection_service import update_recipe_to_collection_service
from app.recipes.services.recipe_service import (
    add_recipe_to_collection_service,
    create_recipe_service,
    embedding_recipes,
    get_all_recipe_service,
    get_issues_recipes,
    get_recipe_by_id_service,
    get_recipes_by_user_id,
    search_recipes_by_embedding,
    update_recipe_service,
    delete_recipe_service,
    set_categories_service,
    ask_order_service,
    update_recipe_to_session_service,
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


@router.get("/macros", status_code=200)
def run_popular_macros():
     popular_macros_para_todas_as_receitas()
     return {"message": "Macros populadas com sucesso"}



def download_and_upload_image(image_url: str, path: str = "") -> str:
    """Baixa uma imagem de uma URL e salva no S3 no diretório especificado por path"""
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        file_extension = image_url.split(".")[-1].split("?")[0] if "." in image_url.split("/")[-1] else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Concatena o caminho, se fornecido
        s3_path = f"{path}/{unique_filename}" if path else unique_filename

        s3_client.upload_fileobj(
            response.raw,  # Envia diretamente do stream para S3
            AWS_BUCKET_NAME,
            s3_path,
            ExtraArgs={"ContentType": f"image/{file_extension}"}
        )

        return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_path}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar e salvar imagem: {str(e)}")

@router.post("/save-image", response_model=ImageDTO, status_code=201)
async def upload_image_to_s3(
    image: UploadFile = File(...),
    path: str = Form("")
) -> ImageDTO:
    try:
        file_extension = image.filename.split(".")[-1]
        file_name = image.filename.split(".")[0]
        unique_filename = f"{file_name}-{uuid.uuid4()}.{file_extension}"

        # Define o caminho no bucket (com subdiretório, se houver)
        s3_path = f"{path}/{unique_filename}" if path else unique_filename

        s3_client.upload_fileobj(
            image.file,
            AWS_BUCKET_NAME,
            s3_path,
            ExtraArgs={"ContentType": image.content_type}
        )

        image_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_path}"
        return ImageDTO(url=image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da imagem para o S3: {str(e)}")

@router.get("/get-ingredients", response_model=List[ImageDTO])
def get_ingredients_images() -> List[ImageDTO]:
    try:
        response = s3_client.list_objects_v2(
            Bucket=AWS_BUCKET_NAME,
            Prefix="ingredients/"
        )

        if "Contents" not in response:
            return []

        images = []
        for obj in response["Contents"]:
            key = obj["Key"]
            if not key.endswith("/"):  # Ignora 'pastas'
                url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
                name = key.split("/")[-1]
                images.append(ImageDTO(url=url, name=name))

        return images

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar imagens de ingredientes: {str(e)}")
    
@router.post("/", response_model=RecipeResponseDTO, status_code=201)
def create_recipe_route(dto: RecipeCreateDTO,user_id: int = Header(..., alias="X-User-Id")):
    try:    
        # Se `image_url` for passado, baixa e salva no S3 antes de criar a receita
        if dto.images[0].url and dto.download_image == True:
            dto.images[0].url = download_and_upload_image(dto.images[0].url)

        recipe = create_recipe_service(dto, user_id=user_id)
        if dto.collection_id:
            add_recipe_to_collection_service(recipe_id=recipe.id, collection_id=dto.collection_id)
        add_recipe_to_session_service(session_id=dto.session_id, recipe_id=recipe.id)
        set_categories_service(recipe.id, dto.categories)
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/{recipe_id}", response_model=RecipeResponseDTO, status_code=200)
def update_recipe_route(recipe_id: int, dto: RecipeCreateDTO):
    try:
        # Se `image_url` for passado, baixa e salva no S3 antes de atualizar a receita
        if dto.images[0].url and dto.download_image == True:
            dto.images[0].url = download_and_upload_image(dto.images[0].url)
        if dto.collection_id:
            update_recipe_to_collection_service(recipe_id=recipe_id,collection_id=dto.collection_id)
        return update_recipe_service(recipe_id=recipe_id, dto=dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/ia_recipe_creator", response_model=RecipeResponseDTO, status_code=201)
def IA_recipe_creator_route(dto: IARecipeCreateDTO):
    try:
        recipe = IA_recipe_creator(dto.title, dto.session_id)
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

@router.post("/filter", status_code=200)
def list_recipe_route(dto: RecipeRequestFilterDTO):
    try:
        return search_recipes_by_embedding(
            query=dto.query,
            page=dto.page,
            size=dto.size,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/{recipe_id}", response_model=RecipeResponseDTO, status_code=200)
def get_recipe_by_id_route(recipe_id: int):
    try:
        return get_recipe_by_id_service(recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.delete("/{recipe_id}", status_code=204)
def delete_recipe_route(recipe_id: int):
    try:
        return delete_recipe_service(recipe_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/embeddings", status_code=200)
def generate_embeddings():
    return embedding_recipes()

@router.post("/ask_order", status_code=200)
def ask_order_route(dto: AskRecipeDTO):
    try:
        return ask_order_service(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



# Rota para adicionar uma receita a uma sessão
SOURCE_PREFIX = ""  # onde estão as imagens originais
TARGET_PREFIX = "images_resized/"  # onde as convertidas serão salvas
@router.post("/resize-all-images")
def resize_and_convert_all_images():
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=AWS_BUCKET_NAME, Prefix=SOURCE_PREFIX)

        processed = []
        errors = []

        for page in page_iterator:
            for obj in page.get("Contents", []):
                key = obj["Key"]

                if not key.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                try:
                    # Extrai o nome do arquivo
                    filename = os.path.basename(key)
                    name_without_ext = os.path.splitext(filename)[0]

                    # Novo caminho no S3
                    new_key = f"{TARGET_PREFIX}{name_without_ext}.webp"

                    # Baixa imagem original
                    img_obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=key)
                    img_bytes = img_obj["Body"].read()

                    # Abre e redimensiona
                    img = PILImage.open(BytesIO(img_bytes)).convert("RGB")
                    img = img.resize((800, 600), PILImage.Resampling.LANCZOS)

                    # Salva em buffer como WebP
                    buffer = BytesIO()
                    img.save(buffer, format="WEBP", quality=85)
                    buffer.seek(0)

                    # Envia para o novo local no S3
                    s3_client.upload_fileobj(
                        buffer,
                        AWS_BUCKET_NAME,
                        new_key,
                        ExtraArgs={"ContentType": "image/webp", "ACL": "public-read"}
                    )

                    processed.append(new_key)

                except UnidentifiedImageError:
                    errors.append({"key": key, "error": "Imagem inválida ou corrompida"})
                except Exception as img_error:
                    errors.append({"key": key, "error": str(img_error)})

        return {
            "message": "Processamento finalizado",
            "total_convertidas": len(processed),
            "total_erros": len(errors),
            "imagens_convertidas": processed,
            "falhas": errors
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fix/issues", status_code=200)
def get_issues_recipes_route():
    try:
        return get_issues_recipes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/users/{user_id}", status_code=200)
def get_user_recipes_route(user_id: int):
    try:
        return get_recipes_by_user_id(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
