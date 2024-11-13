"""relation table

Revision ID: 4be65ab040e8
Revises: f554c58e56d9
Create Date: 2024-11-13 23:58:44.375289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4be65ab040e8"
down_revision: Union[str, None] = "f554c58e56d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_guest_match",
        "guest",  # source table
        "match",  # referenced table
        ["match_seq"],  # source columns
        ["seq"],  # referenced columns
        ondelete="CASCADE",
    )


def downgrade() -> None:
    pass
