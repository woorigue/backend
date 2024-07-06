"""change field of posting

Revision ID: c5f3d9713568
Revises: aec777120c75
Create Date: 2024-07-06 13:30:09.626136

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5f3d9713568"
down_revision: str | None = "aec777120c75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("clubPosting", "status")
    op.drop_column("memberPosting", "status")

    op.add_column(
        "clubPosting",
        sa.Column("closed", sa.Boolean, comment="공고 마감 여부"),
    )
    op.add_column(
        "memberPosting",
        sa.Column("closed", sa.Boolean, comment="공고 마감 여부"),
    )


def downgrade() -> None:
    pass
