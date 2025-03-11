import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração correta para conectar ao PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar o engine para a conexão
engine = create_engine(DATABASE_URL, echo=True)

# Configurar a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()

# Aguardar o banco antes de criar tabelas
def wait_for_db():
    retries = 2
    for i in range(retries):
        try:
            with engine.connect() as conn:
                print("📡 Conectado ao banco de dados!")
                return
        except Exception as e:
            print(f"⏳ Tentando conectar ao banco... ({i+1}/{retries})")
            time.sleep(3)
    print("❌ Banco de dados indisponível. Verifique se ele está rodando.")
    raise Exception("Banco de dados indisponível")

# Aguarda e cria tabelas
wait_for_db()
Base.metadata.create_all(bind=engine)
