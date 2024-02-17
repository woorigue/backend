"""add time field of match model

Revision ID: 1584b05f8ca9
Revises: cc26fb5def4e
Create Date: 2024-02-17 00:01:45.202433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1584b05f8ca9"
down_revision: Union[str, None] = "cc26fb5def4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("match", "match_time", new_column_name="match_date")
    op.add_column(
        "match",
        sa.Column("start_time", sa.Time, comment="매칭 시작 시간"),
    )
    op.add_column(
        "match",
        sa.Column("end_time", sa.Time, comment="매칭 종료 시간"),
    )


def downgrade() -> None:
    op.alter_column("match", "match_date", new_column_name="match_time")
    op.drop_column("match", "start_time")
    op.drop_column("match", "end_time")
