"""add club_seq in poll table

Revision ID: a5c6aaafa619
Revises: ce406bcc42cc
Create Date: 2024-03-09 09:41:39.473740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5c6aaafa619"
down_revision: Union[str, None] = "ce406bcc42cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("poll", sa.Column("club_seq", sa.Integer, comment="클럽 시퀸스"))


def downgrade() -> None:
    op.drop_column("poll", "club_seq")
