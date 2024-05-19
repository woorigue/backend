"""add home/away poll seq in Match

Revision ID: a070c6bdead6
Revises: 78ea277ae45f
Create Date: 2024-04-17 21:36:26.679748

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a070c6bdead6"
down_revision: str | None = "78ea277ae45f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("home_club_poll_seq", sa.Integer, comment="홈 클럽 투표 시퀸스"),
    )
    op.add_column(
        "match",
        sa.Column("away_club_poll_seq", sa.Integer, comment="원정 클럽 투표 시퀸스"),
    )


def downgrade() -> None:
    op.drop_column("match", "home_club_poll_seq")
    op.drop_column("match", "away_club_poll_seq")
