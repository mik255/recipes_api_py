# Usar a imagem base do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar dependências do sistema necessárias e as dependências Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir debugpy \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar o código-fonte e o script de inicialização para o container
COPY ./app /app
COPY ./start.sh /app/start.sh

# Configurar o PYTHONPATH
ENV PYTHONPATH=/app

# Tornar o script executável
RUN chmod +x /app/start.sh

# Expôr as portas da aplicação e do debug
EXPOSE 8000 5678

# Usar o script de inicialização como ponto de entrada
CMD ["sh", "-c", "python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
