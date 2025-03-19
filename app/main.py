import app.init_env as init_env  # ✅ Isso garante que o script execute antes do FastAPI iniciar
from fastapi import FastAPI
from app.recipes.controller import recipes_controller, session_controller,collection_controller, users_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

# app.add_middleware(JWTAuthMiddleware, excluded_paths=["/", "/docs", "/openapi.json", "/sessions/login"])

# Registrar o roteador do módulo Recipe
app.include_router(recipes_controller.router, prefix="/recipes", tags=["Recipes"])
app.include_router(session_controller.router, prefix="/sessions", tags=["Sessions"])
app.include_router(collection_controller.router, prefix="/collections", tags=["collections"])
app.include_router(users_controller.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}
