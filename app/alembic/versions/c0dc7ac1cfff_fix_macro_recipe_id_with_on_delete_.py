"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: c0dc7ac1cfff
Revises: 97eddb371754
Create Date: 2025-03-26 22:35:20.421480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0dc7ac1cfff'
down_revision: Union[str, None] = '97eddb371754'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
