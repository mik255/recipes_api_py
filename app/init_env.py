import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Detectar se está rodando no VS Code
running_in_vscode = "VSCODE_PID" in os.environ or "TERM_PROGRAM" in os.environ

# Definir DEBUG com prioridade:
# 1. Se estiver no VS Code, ativar DEBUG automaticamente.
# 2. Se não estiver no VS Code, usar o valor do .env (ou 'false' por padrão).
DEBUG = running_in_vscode or os.getenv("DEBUG", "false").lower() == "true"

aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
ssm = boto3.client("ssm", region_name="sa-east-1", 
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
)

def get_ssm_param(name):
    """Busca um parâmetro do AWS Systems Manager"""
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]

# Pegando as variáveis do AWS SSM
env_vars = {
    "MEILI_MASTER_KEY": get_ssm_param("MEILI_MASTER_KEY"),
    "BUCKET_NAME": get_ssm_param("BUCKET_NAME"),
    "OPENAI_API_KEY": get_ssm_param("OPENAI_API_KEY"),
    "DATABASE_URL": get_ssm_param("DATABASE_URL")
}

# Se estiver em debug, usa localhost para o Meilisearch
if DEBUG:
    env_vars["MEILI_URL"] = "http://localhost:7700"
else:
    env_vars["MEILI_URL"] = get_ssm_param("MEILI_URL")

# Configurando no os.environ
for key, value in env_vars.items():
    os.environ[key] = value

print(f"🔹 Ambiente configurado com sucesso! Debug: {DEBUG}")
print(f"🔹 Meilisearch URL: {os.environ['MEILI_URL']}")
