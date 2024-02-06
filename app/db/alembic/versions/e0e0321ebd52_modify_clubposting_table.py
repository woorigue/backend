"""modify ClubPosting table

Revision ID: e0e0321ebd52
Revises: 702f43f1b165
Create Date: 2024-01-30 19:23:36.056757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e0e0321ebd52"
down_revision: Union[str, None] = "702f43f1b165"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("clubPosting", "user_seq", new_column_name="writer_user_seq")


def downgrade() -> None:
    op.alter_column("clubPosting", "user_seq", new_column_name="writer_user_seq")
