"""modify match and guest table

Revision ID: 04214ef83305
Revises: ee57845aec3d
Create Date: 2024-02-09 21:55:19.790477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "04214ef83305"
down_revision: Union[str, None] = "168117b089aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("away_club_seq", sa.Integer, nullable=True, comment="원정팀 시퀸스"),
    )
    op.alter_column("match", "club_seq", new_column_name="home_club_seq")
    op.alter_column("match", "guests", new_column_name="guest_seq")

    op.add_column(
        "guest",
        sa.Column("user_seq", sa.Integer, nullable=True, comment="유저 시퀸스"),
    )
    op.alter_column("guest", "club", new_column_name="club_seq")
    op.alter_column("guest", "match", new_column_name="match_seq")


def downgrade() -> None:
    op.drop_column("match", "away_club_seq")
    op.alter_column("match", "home_club_seq", new_column_name="club_seq")
    op.alter_column("match", "guest_seq", new_column_name="guests")

    op.drop_column("guest", "user_seq")
    op.alter_column("guest", "club_seq", new_column_name="club")
    op.alter_column("guest", "match_seq", new_column_name="match")
