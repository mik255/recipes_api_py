import os
import json
from typing import List, Optional

import openai
from pydantic import BaseModel

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from app.recipes.dtos.recipe_dto import RecipeCreateDTO
from app.recipes.repository.recipe_repository import create_recipe
from app.recipes.services.recipe_service import create_recipe_service

# Defina a sua API Key do OpenAI (ideal armazenar em variável de ambiente segura)

llm = OpenAI(temperature=0.3, max_tokens=1024)

# Prompt que instrui o modelo a retornar **somente** o JSON no formato correto
prompt_template = """
Você é um assistente que gera receitas no formato JSON e não pode produzir nada além do JSON.
Se precisar inserir quebras de linha em qualquer texto, use '\\n' (escape de barra invertida).

O JSON deve ter exatamente os campos:
- title (string)
- description (string)
- session_id (int)
- images (lista vazia")
- ingredients (lista de objetos com "description", "title")
- preparations (lista de objetos com "title", "step" (int, em ordem de preparo), "description")

Não inclua texto antes ou depois do objeto JSON, nem use crases (```).
Apenas retorne o objeto JSON puro, com aspas duplas e chaves/colchetes balanceados.

Título da receita: {recipe_title}
Session ID: {session_id}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["recipe_title", "session_id"],
    # output_json=True ou partial_variables={} não é estritamente necessário,
    # mas pode manter se quiser. Aqui está minimalista.
)

chain = LLMChain(llm=llm, prompt=prompt,)

def IA_recipe_creator(title: str, session_id: int):
    # 1. Gera o texto (JSON bruto)
    raw_output = chain.run(recipe_title=title, session_id=session_id)

    print("JSON recebido do LLM:\n", raw_output)

    # 2. Limpa possíveis trechos de markdown, retira espaços extras
    cleaned_output = (
        raw_output
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # 3. Tenta fazer parse do JSON
    try:
        data = json.loads(cleaned_output)
        # 4. Valida e cria o DTO Pydantic
        dto = RecipeCreateDTO(**data)
        
        # 5. Chama seu serviço de criação
        return create_recipe_service(dto)
    except Exception as e:
        print("Erro ao parsear ou salvar receita:", str(e))
        return None
