"""add ondelete cascade to macro.recipe_id

Revision ID: 574a13034607
Revises: 24658acc3c53
Create Date: 2025-03-26 22:13:16.521386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '574a13034607'
down_revision: Union[str, None] = '24658acc3c53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
