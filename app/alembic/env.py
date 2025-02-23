from logging.config import fileConfig
import os
import sys
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.recipes.models import *
# 1) Carrega o objeto de configuração do Alembic
config = context.config

# 2) Se o arquivo de configuração for encontrado, aplica o fileConfig
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3) Importe o seu Base e os modelos, para que o SQLAlchemy
#    conheça todas as tabelas declaradas.
from app.database.config import Base
from app.recipes.models import *  # se você tiver um __init__.py que importa todos

# 4) Define o target_metadata como o Base.metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Executa as migrações em 'offline mode'.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Executa as migrações em 'online mode'.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Seleciona o modo de migração
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
