#!/bin/bash

# Sair do script em caso de erro
set -e

# Exibir logs para depuração
echo "🚀 Configurando ambiente para o FastAPI..."

# **Garantir que o PYTHONPATH está correto**
export PYTHONPATH=/app

# Exibir qual diretório está sendo usado
echo "📂 Diretório atual: $(pwd)"

# Iniciar as migrações do Alembic
echo "🚀 Iniciando migrações do Alembic..."
cd ./app
alembic upgrade head  # ✅ Agora pode rodar direto, pois `alembic.ini` está no lugar certo

# Iniciar o FastAPI
echo "🚀 Iniciando FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
