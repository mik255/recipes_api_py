import os
import openai
import requests

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_direct_image_url(url: str) -> bool:
    return url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))

def get_first_image_google(query: str) -> str:
    query = query + " fundo branco"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": "AIzaSyBy2IMG6IDsXs1M134Elg2nTOXCl6b6R4c",  # ⚠️ Lembre-se de mover isso para um .env!
        "cx": "a3bed842135474db2",
        "q": query,
        "searchType": "image",
        "num": 5  # Aumentado para aumentar chances de imagem válida
    }

    response = requests.get(url, params=params)
    data = response.json()

    for item in data.get("items", []):
        image_url = item.get("link")
        if image_url and is_direct_image_url(image_url):
            correct = validar_imagem_com_chatgpt(image_url, query)
            if correct:
                return image_url

    return None  # Nenhuma imagem válida encontrada

def validar_imagem_com_chatgpt(image_url: str, ingrediente: str) -> bool:
    prompt = f"Essa imagem é uma foto de {ingrediente} como encontramos no supermercado? essa foto tem um fundo branco? Responda com sim ou não sem ponto final"

    response = client.chat.completions.create(
        model="gpt-4o",  # Use a versão vision se quiser usar imagem
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}  # <- aqui é o certo
                ]
            }
        ],
        max_tokens=100
    )

    resposta = response.choices[0].message.content.strip().lower()
    correct = resposta == "sim"
    return correct
