"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: 113b0fba8894
Revises: 3ae3418d04cf
Create Date: 2025-03-26 22:16:03.254309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '113b0fba8894'
down_revision: Union[str, None] = '3ae3418d04cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
