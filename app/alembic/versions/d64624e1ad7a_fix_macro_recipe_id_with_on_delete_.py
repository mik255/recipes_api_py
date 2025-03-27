"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: d64624e1ad7a
Revises: 574a13034607
Create Date: 2025-03-26 22:15:41.266218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd64624e1ad7a'
down_revision: Union[str, None] = '574a13034607'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
