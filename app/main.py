# Inicializando o ambiente antes do FastAPI iniciar
import app.init_env as init_env  # ✅ Isso garante que o script execute antes do FastAPI iniciar

from fastapi import FastAPI, Request
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
app = FastAPI(middleware=middleware, root_path="/", docs_url="/docs", redoc_url="/redoc", strip_slashes=False)

# Importando os controladores (controllers) dos módulos
from app.recipes.controller import (
    recipes_controller,
    session_controller,
    collection_controller,
    users_controller,
)

from app.recipes.controller import mp_getway_controller

# Registrando os roteadores (routers) para os módulos
app.include_router(recipes_controller.router, prefix="/recipes", tags=["Recipes"])
app.include_router(session_controller.router, prefix="/sessions", tags=["Sessions"])
app.include_router(collection_controller.router, prefix="/collections", tags=["Collections"])
app.include_router(users_controller.router, prefix="/users", tags=["Users"])
app.include_router(mp_getway_controller.router, prefix="/payment", tags=["Payment"])

# Rota raiz
@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}

# Debug: Log de todas as requisições para verificar redirecionamentos
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Recebendo requisição: {request.method} {request.url}")
    response = await call_next(request)
    return response
