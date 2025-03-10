"""descrição da migration

Revision ID: ce7d38d98243
Revises: 2971495587b3
Create Date: 2025-02-13 00:09:17.916948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce7d38d98243'
down_revision: Union[str, None] = '2971495587b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipe', 'collection_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('recipe', 'session_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipe', 'session_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('recipe', 'collection_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
