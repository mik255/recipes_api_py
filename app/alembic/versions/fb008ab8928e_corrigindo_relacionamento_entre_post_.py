"""Corrigindo relacionamento entre Post, Midia e PostMidia

Revision ID: fb008ab8928e
Revises: 54c9a646eef5
Create Date: 2025-04-17 23:44:45.336820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb008ab8928e'
down_revision: Union[str, None] = '54c9a646eef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
