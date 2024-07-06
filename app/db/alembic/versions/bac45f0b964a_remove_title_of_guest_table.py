"""remove title of guest table

Revision ID: bac45f0b964a
Revises: 203f77dce831
Create Date: 2024-07-06 13:59:34.949051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bac45f0b964a"
down_revision: Union[str, None] = "203f77dce831"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("guest", "title")


def downgrade() -> None:
    pass
