"""ajuestes

Revision ID: ef3e261d79db
Revises: b27c102ac505
Create Date: 2025-02-23 11:25:25.892808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef3e261d79db'
down_revision: Union[str, None] = 'b27c102ac505'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_recipe')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_recipe',
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], name='session_recipe_recipe_id_fkey'),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], name='session_recipe_session_id_fkey'),
    sa.PrimaryKeyConstraint('recipe_id', 'session_id', name='session_recipe_pkey')
    )
    # ### end Alembic commands ###
