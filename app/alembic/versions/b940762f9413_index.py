"""index

Revision ID: b940762f9413
Revises: e984b9216129
Create Date: 2025-03-25 20:00:07.732858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b940762f9413'
down_revision: Union[str, None] = 'e984b9216129'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_recipe_collection_id'), 'recipe', ['collection_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recipe_collection_id'), table_name='recipe')
    # ### end Alembic commands ###
