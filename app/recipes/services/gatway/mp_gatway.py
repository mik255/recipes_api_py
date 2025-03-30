from datetime import datetime, timedelta
import os
import uuid
import requests
import json

from app.database.dependences import get_db
from app.recipes.models import Order
from app.recipes.models.payment import Payment
from app.recipes.models.plan import Plan
from app.recipes.models.user import User
# Chaves de integração com o Mercado Pago
ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
MERCHANT_URL = 'https://api.mercadopago.com/v1/payments'

def gerar_identificador():
    return f"REF{uuid.uuid4().hex[:6].upper()}"

# Função para criar um pagamento Pix no Mercado Pago
def criar_pagamento_pix(user: User, protocol: str = None, plan_id: int = None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'X-Idempotency-Key': str(uuid.uuid4())
    }

    # Inicia a sessão manualmente (melhor forma fora do contexto FastAPI)
    db = next(get_db())

    try:
        order = db.query(Order).filter(Order.protocol == protocol).first() if protocol else None

        if not plan_id:
            return {"message": "Plan ID is required."}
        
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise Exception("Plano não encontrado.")
        
        if not order:
            protocol = protocol or gerar_identificador()
            order = Order(
                plan_id=plan_id,
                protocol=protocol,
                user_id=user.id,
            )
            db.add(order)
            db.commit()
            db.refresh(order)

        payment = Payment(
            amount=plan.amount,
            method='pix',
            status='pending',
            order_id=order.id,
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        order.payments.append(payment)
        db.commit()
        db.refresh(order)

        # Agora tudo ainda está dentro da mesma sessão
        data = {
            "transaction_amount": plan.amount,
            "payment_method_id": "pix",
            "notification_url": "https://api.mikael.dev.br/payment/notification/",
            "external_reference": protocol,
            "payer": {
                "email": user.email,
                "first_name": user.name,
            },
        }

        response = requests.post(MERCHANT_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            response_data = response.json()
            qr_code = response_data['point_of_interaction']['transaction_data']['qr_code']
            payment_id = response_data['id']

            # Atualiza o objeto dentro da mesma sessão
            payment.getway_payment_id = payment_id
            payment.status = "pending"
            db.commit()
            db.refresh(payment)

            return {
                "qr_code": qr_code,
                "payment_id": payment_id,
                "protocol": protocol,
                "status": "pending",
                "amount": plan.amount,
                "payment_method": "pix",
                "message": "Pagamento Pix criado com sucesso."
            }
        else:
            error_message = response.json().get('message', 'Erro desconhecido')
            raise Exception(f"Erro ao criar pagamento Pix: {error_message}")
    finally:
        db.close()

# Função para atualizar o status do pedido após o pagamento ser confirmado
def atualizar_pagamento(payment_id, status):
    with next(get_db()) as db:
        payment = db.query(Payment).filter(Payment.getway_payment_id == payment_id).first()
        if not payment:
            raise Exception("payment_id não encontrado.")
        if payment:
            payment.status = status
            db.commit()
            db.refresh(payment)
            if status == "payment.approved":
                payment.order.last_payment = datetime.utcnow()
                payment.order.expired_at = payment.order.expired_at + timedelta(days=30)
                payment.status = "approved"
                payment.order.status = "active"
                db.commit()
                db.refresh(payment.order)
            if status == "payment.created":
                payment.order.status = "created"
                db.commit()
                db.refresh(payment.order)
            if status == "payment.cancelled":
                payment.order.status = "cancelled"
                db.commit()
                db.refresh(payment.order)
            if status == "payment.refunded":
                payment.order.status = "refunded"
                db.commit()
                db.refresh(payment.order)
            if status == "payment.in_process":
                payment.order.status = "in_process"
                db.commit()
                db.refresh(payment.order)
                
            return f"pagamento {payment.id} foi atualizado para o status: {status}."
        else:
            raise Exception("Pedido não encontrado para o payment_id fornecido.")

# Função que será chamada pelo webhook para atualizar o pedido no banco de dados
def processar_webhook(payload):
    print("Payload recebido:", payload)
    if payload.get("data") is None:
        payment_id = payload.get("resource")
        return 'Webhook recebido com sucesso'
    
    payment_id = payload.get("data").get("id")
    status = payload.get("action")

    return atualizar_pagamento(payment_id, status)
    

def isActive(user: User):
    with next(get_db()) as db:
        order = (
            db.query(Order)
            .filter(Order.user_id == user.id)
        )

        if not order:
            raise Exception("Nenhum pedido encontrado para o usuário.")

        return [
            {
                "id": order.id,
                "plan_id": order.plan_id,
                "user_id": order.user_id,
                "created_at": order.created_at,
                "last_payment": order.last_payment,
                "expired_at": order.expired_at,
                "status": order.status,
            }
            for order in order
        ]


def get_plans():
    with next(get_db()) as db:
        plans = db.query(Plan).all()
        if not plans:
            raise Exception("Nenhum plano encontrado.")
        return [
            {
                "id": plan.id,
                "name": plan.name,
                "amount": plan.amount,
                "payment_method": 'pix',
                "description": plan.description,
            }
            for plan in plans
        ]

    