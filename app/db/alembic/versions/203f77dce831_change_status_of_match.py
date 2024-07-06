"""change status of match

Revision ID: 203f77dce831
Revises: c5f3d9713568
Create Date: 2024-07-06 13:34:09.275071

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "203f77dce831"
down_revision: str | None = "c5f3d9713568"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("match", "status")
    op.drop_column("guest", "status")

    op.add_column(
        "match",
        sa.Column("matched", sa.Boolean, comment="매칭 여부"),
    )
    op.add_column(
        "guest",
        sa.Column("closed", sa.Boolean, comment="공고 마감 여부"),
    )


def downgrade() -> None:
    pass
