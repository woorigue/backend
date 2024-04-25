"""add accepted column to join club

Revision ID: abffbe477b7a
Revises: 6e01656e5ff1
Create Date: 2024-04-23 22:19:47.404986

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "abffbe477b7a"
down_revision: str | None = "6e01656e5ff1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "join_club",
        sa.Column("accepted", sa.Boolean, comment="수락 여부"),
    )


def downgrade() -> None:
    op.drop_column("join_club", "accepted")
