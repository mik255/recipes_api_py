"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: 97eddb371754
Revises: 520ad2b5ebcb
Create Date: 2025-03-26 22:20:22.640210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97eddb371754'
down_revision: Union[str, None] = '520ad2b5ebcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
