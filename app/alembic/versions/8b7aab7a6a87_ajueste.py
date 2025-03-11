"""ajueste

Revision ID: 8b7aab7a6a87
Revises: 8a969ac5005d
Create Date: 2025-03-01 15:41:01.449652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b7aab7a6a87'
down_revision: Union[str, None] = '8a969ac5005d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_collection', sa.Column('user_id', sa.String(), nullable=False))
    op.drop_constraint('user_collection_user_google_id_fkey', 'user_collection', type_='foreignkey')
    op.create_foreign_key(None, 'user_collection', 'user', ['user_id'], ['id'])
    op.drop_column('user_collection', 'user_google_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_collection', sa.Column('user_google_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user_collection', type_='foreignkey')
    op.create_foreign_key('user_collection_user_google_id_fkey', 'user_collection', 'user', ['user_google_id'], ['google_id'])
    op.drop_column('user_collection', 'user_id')
    # ### end Alembic commands ###
