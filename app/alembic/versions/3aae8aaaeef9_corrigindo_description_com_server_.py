"""Corrigindo description com server_default

Revision ID: 3aae8aaaeef9
Revises: 47cbc691a57a
Create Date: 2025-02-16 09:41:10.199543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aae8aaaeef9'
down_revision: Union[str, None] = '47cbc691a57a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('description', sa.String(), server_default='Sem descrição', nullable=False))
    op.add_column('recipe', sa.Column('preparation_time', sa.Float(), nullable=False))
    op.add_column('recipe', sa.Column('serving_size', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'serving_size')
    op.drop_column('recipe', 'preparation_time')
    op.drop_column('recipe', 'description')
    # ### end Alembic commands ###
