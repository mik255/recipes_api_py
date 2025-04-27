import os
import json
import openai
from sqlalchemy.orm import Session
from app.database.dependences import SessionLocal
from app.recipes.models.ingredient import Ingredient

# Inicializa o cliente da OpenAI com sua API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Template do prompt
ingredient_prompt_template = """
Você é um nutricionista especializado em alimentos e realiza pesquisas reais em supermercados como Carrefour, Pão de Açúcar, Extra, Hortifruti e similares.

Baseado na descrição abaixo, retorne os seguintes campos:

- name: (string) extrair o nome do produto da descrição, corrigir erro de ortografica se nescessário: {description}
- category: (string) Categoria do ingrediente em um supermercado ou loja (ex.: "produtos de limpesa", "hortifruti", "laticínios", "carnes", "padaria", "bebidas", "congelados", "grãos", "temperos","eletronicos","cama, mesa e banho", etc...).
- price: (objeto)
  - quantity: (int) Quantidade padrão para venda (ex.: 1).
  - value: (float) Preço médio real em reais, baseado em supermercados brasileiros confiáveis. Se o valor for abaixo de 1 real, use decimais.
  - unit: (string) Unidade de venda mais comum para o ingrediente deve ser sempre um desses (ex.: "unidade", "kg", "litro", "grama").

Regras obrigatórias:
- O preço deve ser baseado em fontes reais de supermercado, o mais próximo possível da realidade atual.
- Não invente valores. Se não tiver preço exato, estime usando produtos similares.
- Frutas e legumes devem ser precificados por unidade.
- Carnes e grãos devem ser precificados por kg.
- Ingredientes embalados (ex.: arroz, leite) devem ser precificados por kg, unidade ou litro.
- Não use abreviações ou siglas. Use o nome completo do ingrediente.
- Não use aspas ou colchetes. Apenas o JSON puro.
- Responda apenas com o JSON bruto, sem comentários, sem formatação, sem texto adicional.

Descrição:
"{description}"
"""

def build_ingredient_prompt(description: str) -> dict:
    prompt = ingredient_prompt_template.format(description=description)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",  # Melhor para tarefas de alta precisão hoje
        temperature=0.1,             # Reduz variação para evitar preço aleatório
        max_tokens=500,              # Garante que caiba o JSON inteiro
        messages=[{"role": "user", "content": prompt}],
       ## response_format="json"       # Garante que o OpenAI já retorne JSON sem precisar parsear
    )

    raw_json = response.choices[0].message.content
    print(f"\n📙 Ingrediente: {description}\nResposta:\n{raw_json}")

    return json.loads(raw_json)

def popular_dados_ingrediente_por_id(item: Ingredient):
    db: Session = SessionLocal()
    try:
        ing = item
        data = build_ingredient_prompt(ing.description)
        ing.name = data.get("name", "")
        ing.quantity = data.get("price", {}).get("quantity", 0)
        ing.unity = data.get("price", {}).get("unit", "")
        ing.price = data.get("price", {}).get("value", 0.0)
        ing.category = data.get("category",None)
        db.add(ing)
        db.commit()
        print(f"✅ Dados populados para ingrediente ID {ing.id}")
        return ing

    except Exception as e:
        print(f"❌ Erro ao processar ingrediente ID {ing}: {e}")
        db.rollback()
    finally:
        db.close()

def popular_dados_ingredientes():
    db: Session = SessionLocal()
    try:
        ingredients = db.query(Ingredient).filter(
            (Ingredient.quantity == 0) |
            (Ingredient.unity == "unidade") |
            (Ingredient.price == 0) |
            (Ingredient.title == "sem nome")
        ).all()

        for ing in ingredients:
            try:
                data = build_ingredient_prompt(ing.description)

                ing.quantity = data.get("quantity", 0)
                ing.unity = data.get("unity", "")
                ing.name = data.get("name", "")
                ing.price = data.get("estimated_price", 0.0)
                ing.category = data.get("category", "")

                db.add(ing)
                db.commit()
                print(f"✅ Dados populados para ingrediente ID {ing.id}")

            except Exception as e:
                print(f"❌ Erro no ingrediente '{ing.description}': {e}")
                db.rollback()

    finally:
        db.close()

    return "Dados de ingredientes populados com sucesso!"
