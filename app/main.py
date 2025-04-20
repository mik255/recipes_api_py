# Inicializando o ambiente antes do FastAPI iniciar
import app.init_env as init_env  # ✅ Isso garante que o script execute antes do FastAPI iniciar

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Configuração do middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Domínio(s) específico(s)
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

# Instanciando a aplicação FastAPI com middleware
app = FastAPI(middleware=middleware)

# Importando os controladores (controllers) dos módulos
from app.recipes.controller import (
    comments_controller,
    follow_controller,
    likes_controller,
    midia_controller,
    posts_controller,
    recipes_controller,
    session_controller,
    collection_controller,
    users_controller,
    mp_getway_controller
)


# Registrando os roteadores (routers) para os módulos
app.include_router(recipes_controller.router, prefix="/recipes", tags=["Recipes"])
app.include_router(session_controller.router, prefix="/sessions", tags=["Sessions"])
app.include_router(collection_controller.router, prefix="/collections", tags=["Collections"])
app.include_router(users_controller.router, prefix="/users", tags=["Users"])
app.include_router(mp_getway_controller.router, prefix="/payment", tags=["Payment"])

app.include_router(midia_controller.router, prefix="/midia", tags=["Midia"])
app.include_router(follow_controller.router, prefix="/follow", tags=["Follow"])
app.include_router(likes_controller.router, prefix="/like", tags=["Like"])
app.include_router(posts_controller.router, prefix="/post", tags=["Post"])
app.include_router(comments_controller.router, prefix="/comments", tags=["Comments"])


# Rota raiz
@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}
