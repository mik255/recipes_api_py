# Usar a imagem base do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho para o diretório raiz do projeto
WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt .

# Instalar dependências do sistema e as dependências Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar todo o código-fonte para dentro do container
COPY . /app  

# **Configurar o PYTHONPATH corretamente**
ENV PYTHONPATH=/app 

# Tornar o script de inicialização executável
RUN chmod +x /app/start.sh

# Expôr a porta da aplicação
EXPOSE 8000

# Usar o script de inicialização como ponto de entrada
CMD ["/app/start.sh"]
