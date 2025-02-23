#!/bin/bash

# Executar migrações do Alembic
alembic upgrade head

# Iniciar o servidor FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
