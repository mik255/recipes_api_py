import debugpy
from fastapi import FastAPI

from app.recipes.controller import recipes_controller, session_controller,collection_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir apenas o front-end local
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)
# Registrar o roteador do módulo Recipe
app.include_router(recipes_controller.router, prefix="/recipes", tags=["Recipes"])
app.include_router(session_controller.router, prefix="/sessions", tags=["Sessions"])
app.include_router(collection_controller.router, prefix="/collections", tags=["collections"])
@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}
