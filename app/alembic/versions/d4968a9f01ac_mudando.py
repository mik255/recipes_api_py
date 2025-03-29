"""mudando

Revision ID: d4968a9f01ac
Revises: 316423d42661
Create Date: 2025-03-28 18:43:11.152207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4968a9f01ac'
down_revision: Union[str, None] = '316423d42661'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Substitui o alter_column por um SQL direto com USING
    op.execute("""
        ALTER TABLE payment
        ALTER COLUMN getway_payment_id TYPE BIGINT
        USING getway_payment_id::bigint;
    """)


def downgrade() -> None:
    op.alter_column('payment', 'getway_payment_id',
        existing_type=sa.BigInteger(),
        type_=sa.VARCHAR(),
        existing_nullable=True
    )
