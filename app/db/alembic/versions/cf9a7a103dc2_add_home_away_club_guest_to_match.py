"""add  home/away club guest to match

Revision ID: cf9a7a103dc2
Revises: 8d9a2f6695ab
Create Date: 2024-06-25 22:11:13.091689

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cf9a7a103dc2"
down_revision: str | None = "8d9a2f6695ab"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("home_club_guest_seq", sa.Integer, comment="홈 클럽 용병 게시글 시퀸스"),
    )
    op.add_column(
        "match",
        sa.Column("away_club_guest_seq", sa.Integer, comment="원정 클럽 용병 게시글 시퀸스"),
    )
    op.drop_column("match", "guest_seq")


def downgrade() -> None:
    op.drop_column("match", "home_club_guest_seq")
    op.drop_column("match", "away_club_guest_seq")
    op.add_column(
        "match",
        sa.Column("guest_seq", sa.Integer, comment="클럽 용병 게시글 시퀸스"),
    )
