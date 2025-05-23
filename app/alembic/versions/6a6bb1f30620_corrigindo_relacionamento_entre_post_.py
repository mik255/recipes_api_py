"""Corrigindo relacionamento entre Post, Midia e PostMidia

Revision ID: 6a6bb1f30620
Revises: 92cdacb66dc4
Create Date: 2025-04-19 18:13:25.383352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a6bb1f30620'
down_revision: Union[str, None] = '92cdacb66dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_recipe_user_id'), 'recipe', ['user_id'], unique=False)
    op.create_foreign_key(None, 'recipe', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_index(op.f('ix_recipe_user_id'), table_name='recipe')
    op.drop_column('recipe', 'user_id')
    # ### end Alembic commands ###
