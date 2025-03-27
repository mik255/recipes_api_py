"""Fix macro.recipe_id with ON DELETE CASCADE

Revision ID: 520ad2b5ebcb
Revises: 113b0fba8894
Create Date: 2025-03-26 22:17:52.562248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '520ad2b5ebcb'
down_revision: Union[str, None] = '113b0fba8894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
