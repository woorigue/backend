"""add date field to all posting tables

Revision ID: 7421372e6015
Revises: ce8bf0a706f3
Create Date: 2024-02-19 10:12:52.422125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7421372e6015"
down_revision: Union[str, None] = "ce8bf0a706f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "clubPosting",
        sa.Column("date", sa.DateTime, comment="게시일"),
    )
    op.add_column(
        "guest",
        sa.Column("date", sa.DateTime, comment="게시일"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("date", sa.DateTime, comment="게시일"),
    )
    op.add_column(
        "match",
        sa.Column("date", sa.DateTime, comment="게시일"),
    )


def downgrade() -> None:
    op.drop_column("clubPosting", "date")
    op.drop_column("guest", "date")
    op.drop_column("memberPosting", "date")
    op.drop_column("match", "date")
