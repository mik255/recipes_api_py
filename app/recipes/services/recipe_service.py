import os
from typing import List
from fastapi import HTTPException
import openai
import psycopg2

from app.database.dependences import get_db
from app.recipes.dtos.ask_recipe_dto import AskRecipeDTO
from app.recipes.dtos.recipe_dto import RecipeCreateDTO, RecipeListResponseDTO, RecipeRequestFilterDTO
from app.recipes.models.ask_recipe import AskRecipe
from app.recipes.models.category import Category
from app.recipes.models.recipe import Recipe
from app.recipes.models.ingredient import Ingredient
from app.recipes.models.preparation import Preparation
from app.recipes.models.image import Image
from app.recipes.models.session import Session
from app.recipes.repository.collection_repository import get_collection_by_id
from app.recipes.repository.recipe_repository import get_all_recipes, get_recipe_by_id, get_all_sessions
from sqlalchemy.orm import selectinload

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_embedding(texto: str):
    """ Gera o embedding do título + descrição usando OpenAI (versão >= 1.0.0) """
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.embeddings.create(
            input=texto,
            model="text-embedding-3-large"  # Substituir por um modelo mais preciso
        )

        return response.data[0].embedding  # Acessando corretamente os dados da resposta
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return None


def create_recipe_service(recipe_dto: RecipeCreateDTO,user_id:int) -> Recipe:
    """ Cria uma receita, gera embedding e salva no PostgreSQL """
    db = next(get_db())

    new_recipe = Recipe(
        title=recipe_dto.title,
        user_id=user_id,
        description=recipe_dto.description,
        session_id=recipe_dto.session_id,
        preparation_time=recipe_dto.preparation_time,
        dificulty=recipe_dto.dificulty,
        portions=recipe_dto.portions,
        youtube_url=recipe_dto.youtube_url,
        property=recipe_dto.property,
    )
    
    new_recipe.images = [Image(**image.model_dump()) for image in recipe_dto.images]
    new_recipe.ingredients = [Ingredient(**ingredient.model_dump()) for ingredient in recipe_dto.ingredients]
    new_recipe.preparations = [Preparation(**prep.model_dump()) for prep in recipe_dto.preparations]

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Gera embedding do título + descrição
    texto_embedding = f"{new_recipe.title}. {new_recipe.description}"
    embedding = gerar_embedding(texto_embedding)

    if embedding is None:
        print("Erro ao gerar embedding, receita salva sem embedding.")

    # Salvar embedding no banco de dados
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute(
            "UPDATE recipe SET embedding = %s WHERE id = %s",
            (embedding, new_recipe.id)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar embedding no banco: {e}")

    return new_recipe

def set_categories_service(recipe_id: int, categories: list[str]) -> Recipe:
    """ Atualiza as categorias de uma receita """
    with next(get_db()) as db:
        recipe = get_recipe_by_id(db, recipe_id)

        # Buscar categorias no banco pelo nome
        existing_categories = db.query(Category).filter(Category.name.in_(categories)).all()

        # Atualiza as categorias da receita
        recipe.categories = existing_categories
        db.commit()
        db.refresh(recipe)

        return recipe

def get_all_recipe_service() -> list[RecipeListResponseDTO]:
    """ Lista todas as receitas """
    with next(get_db()) as db:
        recipes = get_all_recipes(db)
        return [
            RecipeListResponseDTO(
                id=recipe.id,
                title=recipe.title,
                description=recipe.description,
                tumbnail=recipe.images[0].url if recipe.images else None,
                property=recipe.property
            )
            for recipe in recipes
        ]

def get_recipe_by_id_service(recipe_id: int) -> dict:
    with next(get_db()) as db:
        data = db.query(Recipe).options(
            selectinload(Recipe.images),
            selectinload(Recipe.ingredients),
            selectinload(Recipe.preparations),
            selectinload(Recipe.categories),
            selectinload(Recipe.macro),
        ).filter(Recipe.id == recipe_id).first()

        if not data:
            raise HTTPException(status_code=404, detail="Receita não encontrada.")

        response = data.__dict__.copy()
        response['categories'] = [cat.name for cat in data.categories]
    return response

def update_recipe_service(recipe_id: int, dto: RecipeCreateDTO) -> Recipe:
    """ Atualiza uma receita e o embedding """
    with next(get_db()) as db:
        recipe = get_recipe_by_id(db, recipe_id)
        recipe.title = dto.title
        recipe.description = dto.description
        recipe.images = [Image(url=image.url) for image in dto.images]
        recipe.session_id = dto.session_id
        recipe.preparation_time = dto.preparation_time
        recipe.dificulty = dto.dificulty
        recipe.portions = dto.portions
        recipe.categories = [Category(name=category) for category in dto.categories]
        recipe.ingredients = [Ingredient(title=ingredient.title, description=ingredient.description) for ingredient in dto.ingredients]
        recipe.preparations = [Preparation(title=prep.title, description=prep.description, step=prep.step) for prep in dto.preparations]

        db.commit()
        db.refresh(recipe)

        # Gera novo embedding
        texto_embedding = f"{recipe.title}. {recipe.description}"
        embedding = gerar_embedding(texto_embedding)

        if embedding is not None:
            try:
                conn = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
                cur = conn.cursor()
                cur.execute(
                    "UPDATE recipe SET embedding = %s WHERE id = %s",
                    (embedding, recipe.id)
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Erro ao salvar embedding no banco: {e}")

        return recipe

def delete_recipe_service(recipe_id: int) -> Recipe:
    """ Deleta uma receita """
    with next(get_db()) as db:
        recipe = get_recipe_by_id(db, recipe_id)
        db.delete(recipe)
        db.commit()
    return recipe

def get_sessions() -> list[Session]:
    """ Lista todas as sessões """
    with next(get_db()) as db:
        sessions = get_all_sessions(db)
        return sessions

def add_recipe_to_collection_service(collection_id: int, recipe_id: int):
    """ Adiciona uma receita a uma coleção """
    with next(get_db()) as db:
        collection = get_collection_by_id(db, collection_id)
        recipe = get_recipe_by_id(db, recipe_id)
        collection.recipes.append(recipe)
        db.commit()
        db.refresh(collection)
        return collection

def update_recipe_to_session_service(session_id: int, recipe_id: int):
    """ Atualiza a sessão de uma receita """
    with next(get_db()) as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        session.recipes.remove(recipe)
        session.recipes.append(recipe)
        db.commit()
        db.refresh(session)
        return session

def get_issues_recipes():
    """Busca receitas com problemas:
    - Sem imagem
    - Sem ingredientes ou com ingrediente.title vazio, nulo ou sem 'https'
    - Com description vazia ou nula
    """
    with next(get_db()) as db:
        recipes = db.query(Recipe).options(
            selectinload(Recipe.images),
            selectinload(Recipe.ingredients)
        ).all()

        issues = []
        for recipe in recipes:
            has_invalid_ingredient = any(
                not ingredient.title or "https" not in ingredient.title
                for ingredient in recipe.ingredients
            )

            if not recipe.images or not recipe.ingredients or has_invalid_ingredient or not recipe.description:
                issues.append({
                    "id": recipe.id,
                    "title": recipe.title,
                    "description": recipe.description if recipe.description else "",
                    "tumbnail": recipe.images[0].url if recipe.images else "",  # Pega a primeira imagem, se existir
                    "property": recipe.property if hasattr(recipe, "property") else "admin"  # Garante que "property" exista
                })

        return issues  # Retorna uma lista diretamente




def ask_order_service(dto: AskRecipeDTO):
    """ Serviço para criar pedidos de receitas personalizadas """
    with next(get_db()) as db:
        new_ask_recipe = AskRecipe(description=dto.description)
        db.add(new_ask_recipe)
        db.commit()
        db.refresh(new_ask_recipe)
        return new_ask_recipe
    
def embedding_recipes():
    """ Gera e armazena embeddings para todas as receitas no banco de dados """
    try:
        with next(get_db()) as db:
            recipes = get_all_recipes(db)

            if not recipes:
                return {"message": "Nenhuma receita encontrada para gerar embeddings."}

            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            cur = conn.cursor()

            updated_count = 0
            for recipe in recipes:
                join_ingr = " ".join([ingr.title for ingr in recipe.ingredients])
                join_prep = " ".join([prep.title for prep in recipe.preparations])
                texto_embedding = f"Título: {recipe.title}. Descrição: {recipe.description}. Ingredientes: {join_ingr}. Preparo: {join_prep}"

                # Usa um modelo melhor para gerar embedding
                embedding = gerar_embedding(texto_embedding)

                if embedding:
                    cur.execute(
                        "UPDATE recipe SET embedding = %s WHERE id = %s",
                        (embedding, recipe.id)
                    )
                    updated_count += 1

            conn.commit()
            cur.close()
            conn.close()

            return {"message": f"Embeddings gerados com sucesso para {updated_count} receitas."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

def search_recipes_by_embedding(query: str = "", page: int = 1, size: int = 10):
    """
    Busca receitas similares a uma consulta usando embeddings com paginação real.
    """
    try:
        query = 'receitas do tipo ' + query
        use_embeddings = bool(query.strip())

        if use_embeddings:
            query_embedding = gerar_embedding(query)

        offset = (page - 1) * size

        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        cur = conn.cursor()

        # 1️⃣ Total de registros (sem paginação)
        cur.execute("SELECT COUNT(*) FROM recipe WHERE property != 'user'")
        total_count = cur.fetchone()[0]
        total_pages = (total_count + size - 1) // size

        # 2️⃣ Busca paginada com ou sem embedding
        if not use_embeddings:
            cur.execute("""
                SELECT r.id, r.title, r.description, r.preparation_time, r.portions, r.dificulty, 
                    r.youtube_url, r.property, r.session_id,
                    ARRAY_AGG(i.url) AS image
                FROM recipe r
                LEFT JOIN image i ON i.recipe_id = r.id
                WHERE r.property != 'user'
                GROUP BY r.id
                LIMIT %s OFFSET %s
            """, (size, offset))
        else:
            cur.execute("""
                SELECT r.id, r.title, r.description, r.preparation_time, r.portions, r.dificulty, 
                    r.youtube_url, r.property, r.session_id,
                    ARRAY_AGG(i.url) AS image,
                    r.embedding <=> %s::vector AS distancia
                FROM recipe r
                LEFT JOIN image i ON i.recipe_id = r.id
                WHERE r.property != 'user'
                GROUP BY r.id, distancia
                ORDER BY distancia ASC
                LIMIT %s OFFSET %s
            """, (query_embedding, size, offset))

        results = cur.fetchall()
        cur.close()
        conn.close()

        recipes = [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "preparation_time": row[3],
                "portions": row[4],
                "dificulty": row[5],
                "youtube_url": row[6],
                "property": row[7],
                "session_id": row[8],
                "tumbnail": row[9][0] if row[9] else None,
                "similarity_score": round(row[10], 4) if use_embeddings else None
            }
            for row in results
        ]

        return {
            "total_pages": total_pages,
            "page": page,
            "size": size,
            "recipes": recipes
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar receitas: {str(e)}")

def get_recipes_by_user_id(user_id: int):
    """ Busca receitas de um usuário específico """
    with next(get_db()) as db:
        recipes = db.query(Recipe).filter(Recipe.user_id == user_id).all()
        if not recipes:
            raise HTTPException(status_code=404, detail="Nenhuma receita encontrada para este usuário.")
        return [
            RecipeListResponseDTO(
                id=recipe.id,
                title=recipe.title,
                description=recipe.description,
                tumbnail=recipe.images[0].url if recipe.images else None,
                property=recipe.property
            )
            for recipe in recipes
        ]