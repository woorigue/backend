"""add_join_club__table

Revision ID: 7a6e4a980c35
Revises: 1cdfc9d0487f
Create Date: 2023-11-19 18:42:51.790965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a6e4a980c35"
down_revision: Union[str, None] = "1cdfc9d0487f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "join_club",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("user_seq", sa.Integer),
        sa.Column("clubs_seq", sa.Integer),
    )


def downgrade() -> None:
    op.drop_table("join_club")
