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
Você é um assistente que busca receitas na web a partir do pedido do usuário no formato JSON.
Se precisar inserir quebras de linha em qualquer texto, use '\\n' (escape de barra invertida).
Regras:
1. O JSON deve ser válido e conter todos os campos obrigatórios.
2. Não inclua nenhum texto explicativo, apenas o JSON puro.
3. O JSON deve seguir o modelo de dados definido.
4. Não use formatação Markdown, apenas o JSON puro.
5. nunca reorne objetos vazios, sempre preencha os campos obrigatórios.
6. Não invente informações, use apenas dados reais.
7. Apenas receitas que já foram feitas e aprovadas por usuários reais.
8. Busca receitas que sejam populares e bem avaliadas.

O JSON deve ter exatamente os campos:
- title (string) (nome da receita, não invente um titulo ou nome) 
- description (string)
- session_id (int)
- images (lista vazia")
- ingredients (lista de objetos com "description", "title", "quantity", "unit"(kg, grama, unidade),"price") 
- preparations (lista de objetos com "title", "step" (int, em ordem de preparo), "description")
- portions (int)
- preparation_time (int)
- dificulty (string, um dos valores: "Fácil", "Médio", "Difícil")


Não inclua texto antes ou depois do objeto JSON, nem use crases (```).
Apenas retorne o objeto JSON puro, com aspas duplas e chaves/colchetes balanceados.

pedido do usuário: {recipe_title}
Session ID: {session_id}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["recipe_title", "session_id"],
    # output_json=True ou partial_variables={} não é estritamente necessário,
    # mas pode manter se quiser. Aqui está minimalista.
)

chain = LLMChain(llm=llm, prompt=prompt,)

def IA_recipe_creator(title: str, session_id: int, user_id: int):
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
        dto.property = "user"  # Define a propriedade como 'admin' por padrão
        # 5. Chama seu serviço de criação
        return create_recipe_service(recipe_dto=dto,user_id=user_id)
    except Exception as e:
        print("Erro ao parsear ou salvar receita:", str(e))
        return None
