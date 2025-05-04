import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class StripePaymentService:
    def __init__(self):
        pass

def create_setup_intent(customer_email: str):
    # Tenta encontrar um cliente existente, senão cria
    existing_customers = stripe.Customer.list(email=customer_email).data
    customer = existing_customers[0] if existing_customers else stripe.Customer.create(email=customer_email)
    price = stripe.Price.retrieve(os.getenv("PRICE_ID"))
    payment_intent = stripe.PaymentIntent.create(
            customer=customer.id,
            amount=price.unit_amount,
            currency="brl",
            payment_method_types=["card"],
            setup_future_usage="off_session"  # Isso salva o cartão para uso futuro
        )
    return {
        "customer_id": customer.id,
        "client_secret": payment_intent.client_secret,
        "payment_intent_id": payment_intent.id
    }
    
def create_subscription(customer_id: str, payment_intent_id: str, price_id: str):
    # 1. Buscar o PaymentIntent e extrair o payment_method salvo
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    payment_method_id = payment_intent.payment_method

    if not payment_method_id:
        raise Exception("Nenhum payment_method encontrado no PaymentIntent.")
    
    #verificar se o cliente pagou
    if payment_intent.status != "succeeded":
        return {
            "status": "error",
            "message": "O pagamento não foi concluído com sucesso."
        }

    # 2. Associar esse método de pagamento ao cliente
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # 3. Definir o método como padrão para cobranças futuras
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

    # 4. Criar a assinatura (agora sem payment_intent ou payment_intent_id)
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        default_payment_method=payment_method_id,  # usaremos o ID do método de pagamento
    )

    return {
        "subscription_id": subscription.id,
        "status": subscription.status,
    }
    
def stripe_customer_info_by_email(email):
    """
    Verifica se um cliente com o e-mail fornecido existe na Stripe
    e se possui uma assinatura ativa ou método de pagamento salvo.
    """
    try:
        # Busca clientes com o e-mail informado (pode retornar vários)
        customers = stripe.Customer.search(
            query=f"email:'{email}'",
            limit=1,
        )

        if not customers.data:
            return {
                "customer_exists": False,
                "active": False,
                "has_payment_method": False,
            }

        customer = customers.data[0]
        customer_id = customer.id

        # Verifica se há assinaturas ativas
        subscriptions = stripe.Subscription.list(customer=customer_id, status='all')
        has_active_subscription = any(
            sub['status'] in ['active', 'trialing'] for sub in subscriptions.auto_paging_iter()
        )

        # Verifica se há método de pagamento salvo
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type='card',
        )
        has_payment_method = len(payment_methods.data) > 0

        return {
            "customer_exists": True,
            "active": has_active_subscription,
            "has_payment_method": has_payment_method,
            "customer_id": customer_id,
        }

    except Exception as e:
        raise Exception(f"Erro ao buscar cliente: {str(e)}")
    