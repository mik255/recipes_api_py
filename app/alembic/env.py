import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context

# 🔧 Ajusta o caminho para garantir que os módulos sejam encontrados corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# 📁 Importa os modelos para garantir que o Alembic os reconheça
import app.recipes.models  # Garante que os modelos são carregados corretamente
from app.database.config import Base  # Importa a base do SQLAlchemy

# 🔗 Configuração do Alembic
config = context.config

# 🔧 Carrega a URL do banco de dados da variável de ambiente, se disponível
DATABASE_URL = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

if not DATABASE_URL:
    raise ValueError("❌ ERRO: A variável de ambiente DATABASE_URL não está definida!")

# 🔧 Atualiza a configuração do Alembic com a URL do banco
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 📄 Configuração do log do Alembic (se houver)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🗄 Define os metadados do SQLAlchemy para o Alembic detectar as tabelas
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Executa as migrações no modo offline.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Executa as migrações no modo online.
    """
    # Se a configuração do Alembic usar `alembic.ini`, utilizamos engine_from_config
    if config.get_main_option("sqlalchemy.url"):
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        # Caso contrário, criamos a engine manualmente a partir da variável DATABASE_URL
        connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# 🔥 Executa as migrações no modo correto
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
