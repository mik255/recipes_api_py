import boto3
import os

# Cliente do SSM (Amazon Systems Manager)
ssm = boto3.client("ssm", region_name="sa-east-1", aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
  )

def get_ssm_param(name):
    """Busca um parâmetro do AWS Systems Manager"""
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]

# Pegando as variáveis do AWS SSM
env_vars = {
    "MEILI_URL": get_ssm_param("MEILI_URL"),
    "MEILI_MASTER_KEY": get_ssm_param("MEILI_MASTER_KEY"),
    "BUCKET_NAME": get_ssm_param("BUCKET_NAME"),
    "OPENAI_API_KEY": get_ssm_param("OPENAI_API_KEY"),
    "DATABASE_URL" : get_ssm_param("DATABASE_URL")
}

# Configurando no os.environ
for key, value in env_vars.items():
    os.environ[key] = value

print("Variáveis de ambiente configuradas com sucesso!")

