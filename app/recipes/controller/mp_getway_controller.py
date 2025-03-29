from fastapi import APIRouter, HTTPException, Depends, Header
from app.recipes.services.gatway.mp_gatway import criar_pagamento_pix, get_plans, isActive, processar_webhook
from app.recipes.services.users_service import create_user_service, get_user_by_id,verify_user_exists

# Inicializa o roteador para o módulo Recipe
router = APIRouter()

# Rota para criar um novo REcipe
@router.post("/", status_code=201)
def create_recipe_route(dto: dict):
    try:
        user = verify_user_exists(dto['google_id'])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        return criar_pagamento_pix(
            user=user, 
            protocol=dto.get('protocol'),
            plan_id=dto['plan_id']
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/notification", status_code=200)
def payment_notification_route(dto: dict):
    """
    Recebe a notificação do Mercado Pago e atualiza o status do pedido.
    """
    try:
        # Aqui você deve implementar a lógica para atualizar o status do pedido
        # com base na notificação recebida do Mercado Pago.
        # Exemplo: atualizar_order(dto['id'], dto['status'])
        return processar_webhook(dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/subscription", status_code=200)
def isActive_route(user_id: int = Header(..., alias="X-User-Id")):
    """
    Verifica se o usuário está ativo.
    """
    try:
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Aqui você deve implementar a lógica para verificar se o usuário está ativo
        return isActive(user=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    
@router.get("/plans", status_code=200)
def get_plans_route():
    """
    Verifica se o usuário está ativo.
    """
    try:
        return get_plans()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")