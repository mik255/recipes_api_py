from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth.service.auth import verify_token

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """ Middleware para autenticação via JWT """
    
    def __init__(self, app, excluded_paths=None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/", "/docs", "/openapi.json", "/sessions/login"]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Permitir rotas sem autenticação
        if path in self.excluded_paths:
            return await call_next(request)

        # Verificar token JWT
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return Response("Token JWT não fornecido", status_code=401)

        token = authorization.split("Bearer ")[1]
        try:
            verify_token(token)
        except Exception:
            return Response("Token inválido ou expirado", status_code=401)

        return await call_next(request)
