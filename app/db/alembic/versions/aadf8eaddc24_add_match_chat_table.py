"""add match chat table

Revision ID: aadf8eaddc24
Revises: 374341726008
Create Date: 2024-08-28 01:44:47.299896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aadf8eaddc24"
down_revision: Union[str, None] = "374341726008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
