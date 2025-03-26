import os
import json
import openai
from sqlalchemy.orm import Session
from app.database.dependences import SessionLocal
from app.recipes.models.macros import Macro
from app.recipes.models.recipe import Recipe

# ✅ Criação do cliente OpenAI corretamente
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

macro_prompt_template = """
Você é um nutricionista especializado. Com base na descrição abaixo de uma receita, calcule de forma estimada os macronutrientes e energia.

Retorne um JSON com os seguintes campos:
- total_kcal (int)
- percent_kcal (int): porcentagem da necessidade diária
- carb_percent (int)
- protein_percent (int)
- fiber_percent (int)
- fat_percent (int)

Apenas responda com o JSON. Nenhuma explicação.

Descrição da receita:
"{description}"
"""

def popular_macros_para_todas_as_receitas():
    db: Session = SessionLocal()
    recipes: list[Recipe] = db.query(Recipe).all()

    for recipe in recipes:
        # Skip se já tiver macro associada
        if recipe.macro:
            continue

        prompt = macro_prompt_template.format(description=recipe.description)

        try:
            # ✅ Usando o client corretamente
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )

            raw_json = response.choices[0].message.content
            print(f"\n📘 Receita: {recipe.title}\nResposta:\n{raw_json}")

            data = json.loads(raw_json)

            macro = Macro(
                recipe_id=recipe.id,
                total_kcal=data["total_kcal"],
                percent_kcal=data["percent_kcal"],
                carb_percent=data["carb_percent"],
                protein_percent=data["protein_percent"],
                fiber_percent=data["fiber_percent"],
                fat_percent=data["fat_percent"],
            )

            db.add(macro)
            db.commit()
            print(f"✅ Macros salvos para receita ID {recipe.id}")

        except Exception as e:
            print(f"❌ Erro na receita '{recipe.title}': {e}")
            db.rollback()

    db.close()
