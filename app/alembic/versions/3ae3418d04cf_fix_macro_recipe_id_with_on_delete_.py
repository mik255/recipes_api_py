"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: 3ae3418d04cf
Revises: d64624e1ad7a
Create Date: 2025-03-26 22:15:45.140928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ae3418d04cf'
down_revision: Union[str, None] = 'd64624e1ad7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
