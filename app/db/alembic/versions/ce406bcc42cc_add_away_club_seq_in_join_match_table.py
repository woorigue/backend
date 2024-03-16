"""add away_club_seq in join_match table

Revision ID: ce406bcc42cc
Revises: 0e8b215b1c84
Create Date: 2024-03-07 22:35:35.648117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ce406bcc42cc"
down_revision: Union[str, None] = "0e8b215b1c84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "join_match",
        sa.Column("away_club_seq", sa.Integer, comment="원정팀 시퀸스"),
    )


def downgrade() -> None:
    op.drop_column("join_match", "away_club_seq")
